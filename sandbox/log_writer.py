import os
import json
from datetime import datetime

def write_logs(logs, log_dir="./logs", filename_prefix="session", log_format="json"):
    """
    Writes collected logs to disk in specified format.

    Args:
        logs (list): List of log dictionaries.
        log_dir (str): Directory path to save logs.
        filename_prefix (str): Prefix for the log filename.
        log_format (str): Format to write logs ('json' or 'txt').

    Returns:
        str: Full path to the saved log file.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.{log_format}"
    file_path = os.path.join(log_dir, filename)

    if log_format == "json":
        with open(file_path, "w") as f:
            json.dump(logs, f, indent=2)
    elif log_format == "txt":
        with open(file_path, "w") as f:
            for entry in logs:
                f.write(str(entry) + "\n")
    else:
        raise ValueError(f"Unsupported log format: {log_format}")

    return file_path
