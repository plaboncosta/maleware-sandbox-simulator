from threading import Thread
import time
import random


def start_network_logger(logs):
    """
    Simulates network activity logging in a background thread.

    Args:
        logs (list): Shared log list to append network events

    Returns:
        Thread: The monitoring thread (joinable)
    """

    def simulate_network():
        # Fake outbound network events (simulated)
        fake_hosts = ["8.8.8.8", "192.168.1.1", "example.com", "10.0.0.5", "malicious.site"]
        for _ in range(random.randint(3, 5)):
            ip = random.choice(fake_hosts)
            port = random.choice([80, 443, 8080, 22])
            logs.append({
                "net_event": f"Outbound connection to {ip}:{port}",
                "timestamp": time.time()
            })
            time.sleep(random.uniform(0.5, 1.5))

    thread = Thread(target=simulate_network)
    thread.daemon = True
    thread.start()
    return thread
