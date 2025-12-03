import asyncio
import json
import time
import os

TARGET = "127.0.0.1"
MAX_PORT = 10000
TIMEOUT = 0.5
WORKERS = 500  # semaphore limit (safe concurrency)

sem = asyncio.Semaphore(WORKERS)

async def check_port(target_ip, port):
    async with sem:  # limit concurrency
        try:
            conn = asyncio.open_connection(target_ip, port)
            reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)

            writer.close()
            await writer.wait_closed()

            return port, True

        except:
            return port, False

async def main():
    print(f"\nScanning {TARGET} ...\n")

    start = time.time()

    tasks = [check_port(TARGET, port) for port in range(1, MAX_PORT + 1)]
    results = await asyncio.gather(*tasks)

    open_ports = [p for p, status in results if status]

    end = time.time()
    elapsed = end - start

    print("\n--- Scan Complete ---")
    print("Open ports:", open_ports)
    print(f"Time: {elapsed:.2f} seconds\n")

    with open("results.json", "w") as f:
        json.dump({"open_ports": open_ports}, f, indent=4)


    with open("scan_log.txt", "w") as f:
        f.write("--- Scan Report ---\n")
        f.write(f"Target: {TARGET}\n")
        f.write(f"Scanned ports: 1 - {MAX_PORT}\n")
        f.write(f"Time taken: {elapsed:.2f} seconds\n\n")
        f.write("Open ports:\n")

        if open_ports:
            for p in open_ports:
                f.write(f"  - {p}\n")
        else:
            f.write("  None\n")

    print("Saved scan_log.txt")
    print("Saved results.json")
    print("Location:", os.getcwd())


if __name__ == "__main__":
    asyncio.run(main())
