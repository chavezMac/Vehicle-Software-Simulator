#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOG_ROOT="${PROJECT_ROOT}/logs"
RUN_ID="$(date +%Y%m%d_%H%M%S)"
RUN_LOG_DIR="${LOG_ROOT}/simulation_${RUN_ID}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
START_GATEWAY=true
SETUP_VCAN=true
START_DASHBOARD=false
declare -a SELECTED_ECUS=()
GATEWAY_ONLY=false
GOLDEN_DEMO=false
declare -a DEFAULT_ECUS=(speed door infotainment temperature)
declare -a PIDS=()
declare -a NAMES=()
declare -a LOGS=()
DASHBOARD_PORT=8000
GATEWAY_PORT=5000
WS_PORT=5001
WS_URL="ws://127.0.0.1:${WS_PORT}"
TELEMETRY_VERIFY_DURATION=20

usage() {
  cat <<'EOF'
Usage: scripts/start_simulation.sh [options]

Starts the gateway and selected ECU simulators with per-service logs.

Options:
  --ecus <list>     Comma-separated ECUs: speed,door,infotainment,temperature
  --gateway-only    Start gateway only (no ECUs)
  --no-gateway      Start ECUs only (no gateway)
  --dashboard       Start dashboard static server on port 8000
  --no-vcan         Skip vcan0 setup
  --golden-demo     Print guided golden-demo validation checklist
  --verify-seconds  Telemetry verification window in seconds (default: 20)
  --python <path>   Python executable (default: python3 or $PYTHON_BIN)
  -h, --help        Show this help message

Examples:
  scripts/start_simulation.sh
  scripts/start_simulation.sh --ecus speed,door
  scripts/start_simulation.sh --dashboard
  scripts/start_simulation.sh --golden-demo
  scripts/start_simulation.sh --gateway-only --no-vcan
EOF
}

parse_ecu_list() {
  local csv="$1"
  IFS=',' read -r -a SELECTED_ECUS <<< "${csv}"
}

validate_ecus() {
  local ecu
  if [[ ${#SELECTED_ECUS[@]} -eq 0 ]]; then
    return
  fi
  for ecu in "${SELECTED_ECUS[@]}"; do
    if [[ "${ecu}" != "speed" && "${ecu}" != "door" && "${ecu}" != "infotainment" && "${ecu}" != "temperature" ]]; then
      echo "[error] Unknown ECU '${ecu}'. Valid options: ${DEFAULT_ECUS[*]}" >&2
      exit 1
    fi
  done
}

ecu_script_for() {
  case "$1" in
    speed) echo "ecu/speed_ecu/speed_ecu.py" ;;
    door) echo "ecu/door_ecu/door_ecu.py" ;;
    infotainment) echo "ecu/infotainment_ecu/infotainment_ecu.py" ;;
    temperature) echo "ecu/temperature_ecu/temperature_ecu.py" ;;
    *)
      echo ""
      ;;
  esac
}

print_golden_demo_guide() {
  cat <<EOF
[golden-demo] Validation guide
[golden-demo] Goal: verify speed/door/media/temperature live in Dashboard and IVI.
[golden-demo] Dashboard URL: http://127.0.0.1:8000 (serve with: cd '${PROJECT_ROOT}/dashboard' && ${PYTHON_BIN} -m http.server 8000)
[golden-demo] IVI launch:
[golden-demo]   cd '${PROJECT_ROOT}/ivi/build' && ./ivi_dashboard
[golden-demo]   or: IVI_GATEWAY_URL=ws://127.0.0.1:5001 ./ivi_dashboard
[golden-demo] Acceptance checks:
[golden-demo]   1) In both Dashboard and IVI, each signal updates within 5 seconds:
[golden-demo]      - vehicle_speed, door_open, media_state, temperature
[golden-demo]   2) No crashes: gateway running, dashboard connected, IVI responsive
[golden-demo]   3) No stale telemetry > 10 seconds during steady-state run
[golden-demo]   4) Restart gateway once; clients recover and resume updates within 5-10 seconds
[golden-demo] Artifacts:
[golden-demo]   - Save logs from '${RUN_LOG_DIR}'
[golden-demo]   - Capture dashboard screenshot and IVI screenshot
[golden-demo]   - Fill '${RUN_LOG_DIR}/golden_demo_evidence.md'
[golden-demo] Checklist reference: docs/golden_demo_scenario.md
EOF
}

print_actionable_error() {
  echo "[error] $1" >&2
}

assert_python_dependencies() {
  "${PYTHON_BIN}" - <<'PY'
import importlib
import sys

required = [
    ("can", "python-can"),
    ("flask", "Flask"),
    ("flask_cors", "flask-cors"),
    ("websockets", "websockets"),
]
missing = []
for module_name, package_name in required:
    try:
        importlib.import_module(module_name)
    except Exception:
        missing.append(package_name)

if missing:
    print("Missing Python dependencies: " + ", ".join(missing))
    sys.exit(1)
PY
}

assert_port_free() {
  local port="$1"
  local name="$2"
  "${PYTHON_BIN}" - <<PY
import socket
import sys

port = int("${port}")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sock.bind(("0.0.0.0", port))
except OSError:
    print(f"Port {port} already in use for ${name}")
    sys.exit(1)
finally:
    sock.close()
PY
}

assert_vcan_up() {
  if [[ "$(uname -s)" != "Linux" ]]; then
    return
  fi
  if ! ip link show vcan0 >/dev/null 2>&1; then
    print_actionable_error "vcan0 does not exist. Run with --no-vcan only if a CAN source is already configured."
    exit 1
  fi
  if [[ "$(ip link show vcan0)" != *" UP "* ]]; then
    print_actionable_error "vcan0 exists but is not UP. Run: sudo ip link set up vcan0"
    exit 1
  fi
}

assert_ivi_available_or_build() {
  local ivi_bin="${PROJECT_ROOT}/ivi/build/ivi_dashboard"
  if [[ -x "${ivi_bin}" ]]; then
    return
  fi
  if ! command -v cmake >/dev/null 2>&1; then
    print_actionable_error "IVI binary missing at ${ivi_bin} and cmake not found. Build IVI manually first."
    exit 1
  fi
  if [[ ! -d "${PROJECT_ROOT}/ivi/build" ]]; then
    print_actionable_error "IVI build directory missing at ${PROJECT_ROOT}/ivi/build. Configure/build IVI first."
    exit 1
  fi
  echo "[info] IVI binary missing; attempting build..."
  if ! cmake --build "${PROJECT_ROOT}/ivi/build" >> "${RUN_LOG_DIR}/ivi_build.log" 2>&1; then
    print_actionable_error "IVI build failed. See ${RUN_LOG_DIR}/ivi_build.log"
    exit 1
  fi
  if [[ ! -x "${ivi_bin}" ]]; then
    print_actionable_error "IVI build completed but binary still missing: ${ivi_bin}"
    exit 1
  fi
}

preflight_checks() {
  echo "[info] Running preflight checks..."
  if ! assert_python_dependencies; then
    print_actionable_error "Install dependencies: ${PYTHON_BIN} -m pip install -r requirements.txt"
    exit 1
  fi

  if [[ "${START_GATEWAY}" == "true" ]]; then
    if ! assert_port_free "${GATEWAY_PORT}" "gateway REST"; then
      print_actionable_error "Free port ${GATEWAY_PORT} or stop conflicting process."
      exit 1
    fi
    if ! assert_port_free "${WS_PORT}" "gateway WebSocket"; then
      print_actionable_error "Free port ${WS_PORT} or stop conflicting process."
      exit 1
    fi
  fi

  if [[ "${START_DASHBOARD}" == "true" || "${GOLDEN_DEMO}" == "true" ]]; then
    if ! assert_port_free "${DASHBOARD_PORT}" "dashboard"; then
      print_actionable_error "Free port ${DASHBOARD_PORT} or start dashboard on another port."
      exit 1
    fi
  fi

  if [[ "$(uname -s)" == "Linux" && "${SETUP_VCAN}" != "true" ]]; then
    assert_vcan_up
  fi

  if [[ "${GOLDEN_DEMO}" == "true" ]]; then
    assert_ivi_available_or_build
  fi
}

wait_for_tcp_port() {
  local host="$1"
  local port="$2"
  local timeout="$3"
  "${PYTHON_BIN}" - <<PY
import socket
import sys
import time

host = "${host}"
port = int("${port}")
deadline = time.time() + float("${timeout}")
while time.time() < deadline:
    try:
        with socket.create_connection((host, port), timeout=0.5):
            sys.exit(0)
    except OSError:
        time.sleep(0.2)
print(f"Timeout waiting for {host}:{port}")
sys.exit(1)
PY
}

run_telemetry_contract_check() {
  echo "[info] Running telemetry contract verification (${TELEMETRY_VERIFY_DURATION}s)..."
  if ! "${PYTHON_BIN}" "${PROJECT_ROOT}/scripts/verify_telemetry_contract.py" \
    --url "${WS_URL}" \
    --duration "${TELEMETRY_VERIFY_DURATION}" >> "${RUN_LOG_DIR}/telemetry_verify.log" 2>&1; then
    print_actionable_error "Telemetry contract verification failed. See ${RUN_LOG_DIR}/telemetry_verify.log"
    exit 1
  fi
  echo "[info] Telemetry contract verification passed."
}

write_evidence_template() {
  cat > "${RUN_LOG_DIR}/golden_demo_evidence.md" <<EOF
# Golden Demo Evidence (${RUN_ID})

- Logs directory: ${RUN_LOG_DIR}
- Dashboard URL: http://127.0.0.1:${DASHBOARD_PORT}
- IVI command: cd '${PROJECT_ROOT}/ivi/build' && IVI_GATEWAY_URL=${WS_URL} ./ivi_dashboard

## Checklist

- [ ] Dashboard reached Live status and all fields updated
- [ ] IVI launched and all fields updated
- [ ] Telemetry contract check passed
- [ ] Gateway restart recovery validated (5-10s)
- [ ] Fault injection validated (stop one ECU, restart it)

## Artifacts

- Dashboard screenshot path:
- IVI screenshot path:
- Notes:
- Final result: PASS/FAIL
EOF
}

print_run_contract() {
  local i
  echo "[info] Run contract:"
  for i in "${!NAMES[@]}"; do
    echo "  - ${NAMES[$i]} pid=${PIDS[$i]} log=${LOGS[$i]}"
  done
  echo "  - Dashboard URL: http://127.0.0.1:${DASHBOARD_PORT}"
  echo "  - IVI command: cd '${PROJECT_ROOT}/ivi/build' && IVI_GATEWAY_URL=${WS_URL} ./ivi_dashboard"
}

setup_vcan() {
  if [[ "${SETUP_VCAN}" != "true" ]]; then
    echo "[info] Skipping vcan setup (--no-vcan)."
    return
  fi

  if [[ "$(uname -s)" != "Linux" ]]; then
    echo "[warn] vcan setup requested, but this host is not Linux. Skipping."
    return
  fi

  echo "[info] Ensuring vcan0 is available..."
  sudo modprobe vcan
  if ! ip link show vcan0 >/dev/null 2>&1; then
    sudo ip link add dev vcan0 type vcan
  fi
  sudo ip link set up vcan0
}

start_process() {
  local name="$1"
  shift
  local log_file="${RUN_LOG_DIR}/${name}.log"

  "$@" >> "${log_file}" 2>&1 &
  local pid=$!

  PIDS+=("${pid}")
  NAMES+=("${name}")
  LOGS+=("${log_file}")
  echo "[start] ${name} (pid=${pid}) -> ${log_file}"
}

cleanup() {
  local i pid name
  for i in "${!PIDS[@]}"; do
    pid="${PIDS[$i]}"
    name="${NAMES[$i]}"
    if kill -0 "${pid}" >/dev/null 2>&1; then
      echo "[stop] ${name} (pid=${pid})"
      kill "${pid}" >/dev/null 2>&1 || true
    fi
  done
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ecus)
      if [[ $# -lt 2 ]]; then
        echo "[error] --ecus requires a comma-separated value." >&2
        exit 1
      fi
      parse_ecu_list "$2"
      GATEWAY_ONLY=false
      shift 2
      ;;
    --gateway-only)
      SELECTED_ECUS=()
      GATEWAY_ONLY=true
      shift
      ;;
    --no-gateway)
      START_GATEWAY=false
      shift
      ;;
    --no-vcan)
      SETUP_VCAN=false
      shift
      ;;
    --dashboard)
      START_DASHBOARD=true
      shift
      ;;
    --golden-demo)
      GOLDEN_DEMO=true
      START_DASHBOARD=true
      shift
      ;;
    --verify-seconds)
      if [[ $# -lt 2 ]]; then
        echo "[error] --verify-seconds requires a value." >&2
        exit 1
      fi
      TELEMETRY_VERIFY_DURATION="$2"
      shift 2
      ;;
    --python)
      if [[ $# -lt 2 ]]; then
        echo "[error] --python requires a path." >&2
        exit 1
      fi
      PYTHON_BIN="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[error] Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ ${#SELECTED_ECUS[@]} -eq 0 && "${START_GATEWAY}" == "true" && "${GATEWAY_ONLY}" != "true" ]]; then
  SELECTED_ECUS=("${DEFAULT_ECUS[@]}")
fi

if [[ "${START_GATEWAY}" != "true" && ${#SELECTED_ECUS[@]} -eq 0 ]]; then
  echo "[error] Nothing to run. Enable gateway and/or select ECUs." >&2
  exit 1
fi

validate_ecus

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "[error] Python executable not found: ${PYTHON_BIN}" >&2
  exit 1
fi

mkdir -p "${RUN_LOG_DIR}"
preflight_checks
setup_vcan
if [[ "$(uname -s)" == "Linux" ]]; then
  assert_vcan_up
fi

echo "[info] Logs directory: ${RUN_LOG_DIR}"
echo "[info] Python executable: ${PYTHON_BIN}"
echo "[info] Selected ECUs: ${SELECTED_ECUS[*]:-(none)}"
if [[ "${GOLDEN_DEMO}" == "true" ]]; then
  print_golden_demo_guide
fi

trap cleanup INT TERM EXIT

if [[ "${START_GATEWAY}" == "true" ]]; then
  start_process "gateway" bash -lc "cd '${PROJECT_ROOT}/gateway' && '${PYTHON_BIN}' vehicle_gateway.py"
fi

for ecu in "${SELECTED_ECUS[@]}"; do
  ecu_script="$(ecu_script_for "${ecu}")"
  start_process "${ecu}_ecu" bash -lc "cd '${PROJECT_ROOT}' && '${PYTHON_BIN}' '${ecu_script}'"
done

if [[ "${START_DASHBOARD}" == "true" ]]; then
  start_process "dashboard" bash -lc "cd '${PROJECT_ROOT}/dashboard' && '${PYTHON_BIN}' -m http.server ${DASHBOARD_PORT}"
fi

if [[ "${START_GATEWAY}" == "true" ]]; then
  if ! wait_for_tcp_port "127.0.0.1" "${GATEWAY_PORT}" "10"; then
    print_actionable_error "Gateway REST did not become ready on port ${GATEWAY_PORT}"
    exit 1
  fi
  if ! wait_for_tcp_port "127.0.0.1" "${WS_PORT}" "10"; then
    print_actionable_error "Gateway WebSocket did not become ready on port ${WS_PORT}"
    exit 1
  fi
fi

if [[ "${GOLDEN_DEMO}" == "true" ]]; then
  run_telemetry_contract_check
  write_evidence_template
fi

print_run_contract
echo "[info] Simulation running. Press Ctrl+C to stop all processes."
wait
