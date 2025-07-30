import os
import resource
import subprocess
from datetime import datetime
import json

from sandbox import filesystem_monitor, network_logger


def set_limits(memory_limit_mb):
    """
    Apply a memory limit for the child process (Unix only).
    """
    memory_bytes = memory_limit_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))


def run_sample(sample_path, config):
    """
    Runs a sample in a restricted subprocess and collects log outputs.

    Args:
        sample_path (str): Path to the executable sample
        config (dict): Configuration settings (timeout, log path, etc.)

    Returns:
        list: Collected behavior logs (stdout, stderr, file, net events)
    """
    logs = []
    sandbox_config = config["sandbox"]
    timeout = sandbox_config["timeout_seconds"]
    memory_limit = sandbox_config["memory_limit_mb"]
    log_dir = sandbox_config.get("log_directory", "./logs")
    os.makedirs(log_dir, exist_ok=True)

    # Start filesystem & network monitoring threads with shared logs
    fs_logs = []
    net_logs = []

    # Start monitoring threads for duration = timeout seconds
    fs_thread = filesystem_monitor.start_fs_monitor(fs_logs, path="./samples", monitor_duration=timeout)
    net_thread = network_logger.start_network_logger(net_logs)

    try:
        # Run the sample in a sandboxed subprocess
        proc = subprocess.Popen(
            ["python3", sample_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=lambda: set_limits(memory_limit)
        )

        stdout, stderr = proc.communicate(timeout=timeout)
        logs.append({"stdout": stdout.strip()})
        logs.append({"stderr": stderr.strip()})
    except subprocess.TimeoutExpired:
        proc.kill()
        logs.append({"error": "Sample execution timed out."})
    except Exception as e:
        logs.append({"error": str(e)})

    # Wait for monitoring threads to finish cleanly
    fs_thread.join(timeout=1)
    net_thread.join(timeout=1)

    # Combine logs from monitors
    logs.extend(fs_logs)
    logs.extend(net_logs)

    # Save combined logs to file (fix typo: indent)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = os.path.join(log_dir, f"session_{ts}.json")
    with open(log_file_path, 'w') as f:
        json.dump(logs, f, indent=2)

    return logs
