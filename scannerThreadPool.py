import socket
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from itertools import repeat
import os
import json



TARGET = "127.0.0.1" #localhost
WORKERS = 250
TIMEOUT = 0.5
MAX_PORT = 10000

def check_port(target_ip, port1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)

    try:
        sock.connect((target_ip, port1))
        return port1, True

    except:
        return port1, False
    finally:
        sock.close()


if __name__ == "__main__":
    target = TARGET

    open_ports = []
    closed_count = 0
    ports = range(1, MAX_PORT + 1)

    start_time = time.time()

    print(f"\nScanning {target}...\n")

    with ThreadPoolExecutor (max_workers=WORKERS) as executor:
        for port, is_open in executor.map(check_port,repeat(target), ports):
            if is_open:
                print(f"[+] Port {port} OPEN")
                open_ports.append(port)
            else:
                closed_count += 1

    print("\nScan complete!")

    end_time = time.time()
    total_time = end_time - start_time

    print("\n--- Scan Complete ---")
    print(f"Open ports: {open_ports}")
    print(f"Time taken: {total_time:.2f} seconds\n")

    with open("results.json", "w") as f:
        json.dump({"open_ports": open_ports}, f, indent=4)
    with open("scan_log.txt", "w") as f:
        f.write("--- Scan Report ---\n")
        f.write(f"Target: {TARGET}\n")
        f.write(f"Scanned ports: 1 - {MAX_PORT}\n")
        f.write(f"Time taken: {total_time:.2f} seconds\n\n")
        f.write("Open ports:\n")

        if open_ports:
            for p in open_ports:
                f.write(f"  - {p}\n")
        else:
            f.write("  None\n")

    print("Saved scan_log.txt")
    print("Saving in:", os.getcwd())
    print("Saved results.json")
