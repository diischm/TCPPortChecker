import asyncio
import time
import json
import os

TARGET = "127.0.0.1"
TIMEOUT = 0.5
MAX_PORT = 10000


async def check_port(port):
    try:
        conn = asyncio.open_connection(TARGET, port)
        reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)
        writer.close()
        return port, True
    except:
        return port, False


async def main():
    print(f"\nScanning {TARGET} with asyncio...\n")
    start_time = time.time()

    open_ports = []
    closed_count = 0

    tasks = [check_port(port) for port in range(1, MAX_PORT + 1)]

    for coro in asyncio.as_completed(tasks):
        port, is_open = await coro

        if is_open:
            print(f"[+] Port {port} OPEN")
            open_ports.append(port)
        else:
            closed_count += 1

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


if __name__ == "__main__":
    asyncio.run(main())
