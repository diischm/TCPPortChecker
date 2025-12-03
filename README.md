# Python TCP Port Scanner Comparison **Disclaimer:** This project is intended **only for educational purposes** and should be run **only on your own machine**.
 This repository contains **three Python scripts** that scan for open TCP ports on the user's local machine (`localhost`). Each script demonstrates a different concurrency approach, allowing you to compare **runtime efficiency and accuracy**.
 ---
 ## My Learning Journey
 This project began as a way for me to **improve my Python skills** for network programming. Firstly, I wrote a simple port scanner using a sequential `for`-loop, but scanning thousands of ports was extremely slow. This led me to explore **different concurrency techniques**: 1. **ThreadPool:** Improved runtime by checking multiple ports concurrently. I learned how Python threads work and how I/O-bound tasks can bypass the Global Interpreter Lock (GIL).
 2. **Asyncio:** Enabled thousands of tasks to run concurrently in a single-threaded event loop. I learned about asynchronous programming and event-driven design, as well as the potential pitfalls of extreme concurrency.
 3. **Asyncio with Semaphore:** Balanced speed and reliability by limiting concurrency. I learned how semaphores can control task execution without blocking the event loop.
 ---
 ## 1. ThreadPool
 ThreadPool significantly improves runtime compared to a naive sequential method.
 - **Naive method:** Checks ports one by one, keeping the CPU mostly idle.
 - **ThreadPool:** Uses multiple threads to check ports concurrently, improving efficiency for I/O-bound tasks.
 ### Script
 ```python
 import socket
 import threading
 import time
 from concurrent.futures.thread import ThreadPoolExecutor from itertools import repeat import os
 import json
 TARGET = "127.0.0.1"
 WORKERS = 250
 TIMEOUT = 0.5
 MAX_PORT = 10000
 def check_port(target_ip, port1): sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) sock.settimeout(TIMEOUT) try:
 sock.connect((target_ip, port1)) return port1, True
 except:
 return port1, False
 finally:
 sock.close()
 if __name__ == "__main__": target = TARGET
 open_ports = []
 closed_count = 0
 ports = range(1, MAX_PORT + 1) start_time = time.time() print(f"\nScanning {target}...\n") with ThreadPoolExecutor(max_workers=WORKERS) as executor: for port, is_open in executor.map(check_port, repeat(target), ports): if is_open:
 print(f"[+] Port {port} OPEN") open_ports.append(port)
 else:
 closed_count += 1
 print("\nScan complete!") end_time = time.time()
 total_time = end_time - start_time print("\n--- Scan Complete ---") print(f"Open ports: {open_ports}") print(f"Time taken: {total_time:.2f} seconds\n") with open("results.json", "w") as f: json.dump({"open_ports": open_ports}, f, indent=4) ```
 ---
 ## 2. Asyncio
 Asyncio runs thousands of tasks concurrently in a single-threaded event loop, providing high efficiency.
 ### Script
 ```python
 import asyncio
 import time
 import json
 import os
 TARGET = "127.0.0.1"
 TIMEOUT = 0.5
 MAX_PORT = 10000
 async def check_port(port): try:
 conn = asyncio.open_connection(TARGET, port) reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT) writer.close()
 return port, True
 except:
 return port, False
 async def main():
 print(f"\nScanning {TARGET} with asyncio...\n") start_time = time.time() open_ports = []
 closed_count = 0
 tasks = [check_port(port) for port in range(1, MAX_PORT + 1)] for coro in asyncio.as_completed(tasks): port, is_open = await coro if is_open:
 print(f"[+] Port {port} OPEN") open_ports.append(port)
 else:
 closed_count += 1
 end_time = time.time()
 total_time = end_time - start_time print("\n--- Scan Complete ---") print(f"Open ports: {open_ports}") print(f"Time taken: {total_time:.2f} seconds\n") with open("results.json", "w") as f: json.dump({"open_ports": open_ports}, f, indent=4) if __name__ == "__main__": asyncio.run(main())
 ```
 ---
 ## 3. Asyncio with Semaphore Adds a concurrency cap for improved accuracy while retaining speed.
 ### Script
 ```python
 import asyncio
 import json
 import time
 import os
 TARGET = "127.0.0.1"
 MAX_PORT = 10000
 TIMEOUT = 0.5
 WORKERS = 500
 sem = asyncio.Semaphore(WORKERS) async def check_port(target_ip, port): async with sem:
 try:
 conn = asyncio.open_connection(target_ip, port) reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT) writer.close()
 await writer.wait_closed() return port, True
 except:
 return port, False
 async def main():
 print(f"\nScanning {TARGET} ...\n") start = time.time()
 tasks = [check_port(TARGET, port) for port in range(1, MAX_PORT + 1)] results = await asyncio.gather(*tasks) open_ports = [p for p, status in results if status] end = time.time()
 elapsed = end - start
 print("\n--- Scan Complete ---") print("Open ports:", open_ports) print(f"Time: {elapsed:.2f} seconds\n") with open("results.json", "w") as f: json.dump({"open_ports": open_ports}, f, indent=4) if __name__ == "__main__": asyncio.run(main())
 ```
 ---
 ## Summary
 | Method | Pros | Cons | |--------|------|------| | ThreadPool | Faster than loop, uses I/O concurrency | Slower than asyncio | | Asyncio | Extremely fast, thousands of tasks | May miss ports under heavy load | | Asyncio + Semaphore | Balanced & accurate | Slightly slower | > Compare Python concurrency methods (ThreadPool, Asyncio, Asyncio+Semaphore) for scanning open TCP ports on your own machine. **Educational use only.**
