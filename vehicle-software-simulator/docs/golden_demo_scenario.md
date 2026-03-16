# Golden Demo Scenario (Phase 1, Step 4)

This document defines one repeatable "golden demo path" for the simulator.
Use it as the pass/fail contract before moving to later phases.

## Golden Scenario

```text
GoldenScenario:
  speed changes every ~1s
  door toggles open/closed periodically
  media cycles STOPPED/PLAYING/PAUSED
  temperature changes periodically
```

## Expected UI Behavior

```text
ExpectedUI:
  Dashboard shows 4 values updating without refresh
  IVI shows same 4 values updating without restart
  If gateway restarts, clients reconnect and resume updates
```

## Acceptance Criteria

Use `N = 5 seconds`.

1. **Signal freshness in both UIs**
   - In the Dashboard and IVI, each of the four signals updates at least once within 5 seconds of observation:
     - `vehicle_speed`
     - `door_open`
     - `media_state`
     - `temperature`

2. **No crash condition**
   - Gateway process remains running.
   - Dashboard page remains connected (or reconnects automatically).
   - IVI app remains running (no crash, freeze, or forced restart).

3. **No stale telemetry beyond timeout**
   - During steady-state demo operation, no signal remains unchanged for more than `10 seconds` unless intentionally paused for a test.
   - If any signal is stale for >10 seconds, mark the run as failed and inspect ECU/gateway logs.

4. **Gateway restart resilience**
   - After intentionally restarting the gateway, both Dashboard and IVI reconnect and resume live updates within `5-10 seconds`.

## Quick Pass/Fail Checklist

```text
RunResult:
  dashboardLive: PASS/FAIL
  iviLive: PASS/FAIL
  speedFresh: PASS/FAIL
  doorFresh: PASS/FAIL
  mediaFresh: PASS/FAIL
  temperatureFresh: PASS/FAIL
  gatewayRestartRecovery: PASS/FAIL
  crashesObserved: YES/NO
```

If all checks are PASS and `crashesObserved` is NO, the golden demo path is accepted.

## Preflight Checks (Before Launch)

The launcher enforces these checks before starting demo processes:

- Python dependencies installed (`python-can`, `Flask`, `flask-cors`, `websockets`)
- Ports are free:
  - `5000` (gateway REST)
  - `5001` (gateway WebSocket)
  - `8000` (dashboard static server)
- On Linux:
  - `vcan0` exists and is `UP` (or launcher brings it up when `--no-vcan` is not used)
- IVI readiness for golden demo:
  - `ivi/build/ivi_dashboard` exists, or launcher attempts `cmake --build ivi/build`

If a check fails, launcher prints an actionable error and exits without launching processes.

## Telemetry Contract Verification

`scripts/verify_telemetry_contract.py` performs a 20-second verification loop:

- Connects to `ws://127.0.0.1:5001`
- For each snapshot:
  - asserts keys: `vehicle_speed`, `door_open`, `media_state`, `temperature`
  - asserts types:
    - `vehicle_speed` -> number
    - `door_open` -> bool
    - `media_state` -> string in `STOPPED|PLAYING|PAUSED`
    - `temperature` -> number
- Tracks field value changes over the window
- Passes only if all 4 fields change at least once

## Dashboard Verification Steps (Manual)

1. Open `http://127.0.0.1:8000`
2. Wait for status text to show `Live`
3. Observe for 30 seconds:
   - speed changes
   - door toggles
   - media cycles states
   - temperature changes
4. Fail the run if any field never updates

Optional visual checks:
- Connection indicator is green/live
- Displayed values use readable units/labels

## IVI Verification Steps (Manual)

1. Launch IVI:
   - `cd ivi/build`
   - `IVI_GATEWAY_URL=ws://127.0.0.1:5001 ./ivi_dashboard`
2. Verify main view renders and stays responsive
3. Observe for 30 seconds:
   - speed/door/media/temp all update
4. Restart gateway once and confirm IVI resumes updates within 5-10 seconds

## Fault Injection (Manual)

Test resilience by stopping one ECU, for example media ECU:

1. Stop media ECU process
2. Expected:
   - speed/door/temp continue updating
   - system remains stable (no crashes)
   - media value remains stable (stale) until ECU restarts
3. Restart media ECU
4. Expected:
   - media updates resume

## Evidence Capture

For each golden run:

- Save launcher logs directory path
- Capture dashboard screenshot
- Capture IVI screenshot
- Save short terminal transcript
- Record final PASS/FAIL with timestamp

Launcher creates an evidence template at:
- `logs/simulation_<timestamp>/golden_demo_evidence.md`

## One-Command Golden Demo Contract

Run:

- `scripts/start_simulation.sh --golden-demo`

Behavior:

- Starts gateway, selected ECUs, and dashboard
- Prints process IDs and log file paths
- Prints dashboard URL and IVI launch command
- Runs telemetry contract verification
- Blocks until `Ctrl+C`
- On `Ctrl+C`, cleanly stops all child processes

## Done Criteria (Phase 1, Step 4)

Phase 1 Step 4 is complete when:

- Golden demo launcher runs successfully
- Telemetry contract verification passes
- Dashboard and IVI manual checks pass
- Gateway restart recovery is validated
- Fault injection test is validated
- Evidence file is completed and marked PASS
