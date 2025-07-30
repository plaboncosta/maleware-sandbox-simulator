from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread
import time
import os

class FSMonitorHandler(FileSystemEventHandler):
    def __init__(self, logs):
        self.logs = logs

    def on_created(self, event):
        if not event.is_directory:
            self.logs.append({"fs_event": f"Created: {event.src_path}"})

    def on_modified(self, event):
        if not event.is_directory:
            self.logs.append({"fs_event": f"Modified: {event.src_path}"})

    def on_deleted(self, event):
        if not event.is_directory:
            self.logs.append({"fs_event": f"Deleted: {event.src_path}"})


def start_fs_monitor(logs, path="./samples", monitor_duration=10):
    """
    Starts a background thread to monitor filesystem events.

    Args:
        logs (list): Shared list to append fs events
        path (str): Directory to monitor
        monitor_duration (int): Seconds to keep the monitor running

    Returns:
        Thread: Stopper thread to clean up observer after timeout
    """
    if not os.path.exists(path):
        os.makedirs(path)

    event_handler = FSMonitorHandler(logs)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    # Start the observer in a separate thread
    observer_thread = Thread(target=observer.start)
    observer_thread.daemon = True
    observer_thread.start()

    # Stop the observer after the specified duration
    def stop_after_delay():
        time.sleep(monitor_duration)
        observer.stop()
        observer.join()

    stopper_thread = Thread(target=stop_after_delay)
    stopper_thread.start()

    return stopper_thread
