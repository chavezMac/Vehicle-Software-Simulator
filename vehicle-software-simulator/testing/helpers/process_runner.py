import os
import subprocess

from pathlib import Path

_ROOT_DIR = Path(__file__).resolve().parents[2]
_GATEWAY_DIR = _ROOT_DIR / "gateway"
_TEST_LOG_DIR = _ROOT_DIR / "logs" / "test_runs"

class ProcessGroup:

    def __init__(self):
        self.children = []
    
    def start_gateway(self):
        
        script_dir = _GATEWAY_DIR
        arguments = [os.environ.get("PYTHON_BIN", "python3"), "vehicle_gateway.py"]

        _TEST_LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_path = _TEST_LOG_DIR / "gateway_test.log"
        log_file = open(log_path, "a", encoding="utf-8")
        
        # cmd = ["python3", "vehicle_gateway.py"]
        proc = subprocess.Popen(
            arguments,
            cwd=str(script_dir),
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
        )
        # stdout/stderr -> temp log files
        print(f"Started gateway (pid={proc.pid}) -> {log_path}")

        #append proc to self.children
        self.children.append(proc)
        return proc

    def start_ecu(self, name):
        valid_names = {"speed", "door", "infotainment", "temperature"}
        if name not in valid_names:
            raise ValueError(f"Unknown ECU: {name}")

        _TEST_LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_path = _TEST_LOG_DIR / f"{name}_ecu_test.log"
        log_file = open(log_path, "a", encoding="utf-8")

        # cmd = ["python3", f"ecu/{name}_ecu/{name}_ecu.py"]
        arguments = [
            os.environ.get("PYTHON_BIN", "python3"),
            f"ecu/{name}_ecu/{name}_ecu.py",
        ]

        proc = subprocess.Popen(
            arguments,
            cwd=str(_ROOT_DIR),
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print(f"Started {name} ECU (pid={proc.pid}) -> {log_path}")

        # append proc
        self.children.append(proc)
        return proc
    
    def stop_all(self):
        for proc in self.children:
            if proc is None:
                continue

            if proc.poll() is not None:
                continue

            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)

        self.children.clear()