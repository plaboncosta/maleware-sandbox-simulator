import os
from datetime import datetime

def generate_report(logs, report_dir="./report", filename_prefix="session"):
    """
    Generates a Markdown report summarizing sandbox logs.

    Args:
        logs (list): List of log dicts collected during sandbox run.
        report_dir (str): Directory to save report file.
        filename_prefix (str): Prefix for report filename.

    Returns:
        str: Full path to the saved report file.
    """
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.md"
    filepath = os.path.join(report_dir, filename)

    # Aggregate stats
    fs_events = [entry['fs_event'] for entry in logs if 'fs_event' in entry]
    net_events = [entry['net_event'] for entry in logs if 'net_event' in entry]

    with open(filepath, "w") as f:
        f.write(f"# Malware Sandbox Analysis Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write(f"## Summary\n")
        f.write(f"- Total filesystem events: {len(fs_events)}\n")
        f.write(f"- Total network events: {len(net_events)}\n\n")

        f.write("## Filesystem Activity\n")
        if fs_events:
            for event in fs_events:
                f.write(f"- {event}\n")
        else:
            f.write("No filesystem events recorded.\n")
        f.write("\n")

        f.write("## Network Activity\n")
        if net_events:
            for event in net_events:
                f.write(f"- {event}\n")
        else:
            f.write("No network events recorded.\n")

    return filepath
