import socket
import time
from concurrent.futures import ThreadPoolExecutor
from protocol import send_msg, recv_msg

CONFIG_FILE = "machines.txt"
TIMEOUT_SECONDS = 2

def load_machines(filename):
    machines = []
    with open(filename) as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            host, port = line.split(':')
            machines.append((host, int(port)))


    return machines

def query_machine(host, port, pattern):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT_SECONDS)
            s.connect((host, port))
            send_msg(s, pattern.encode())
            data = recv_msg(s)
            lines = data.decode().splitlines()

            return {
                "host": host,
                "port": port,
                "success": True,
                "lines": lines,
                "count": len(lines)
            }
    except socket.timeout:
        return {
            "host": host,
            "port": port,
            "success": False,
            "error": "timed out"
        }
    
    except ConnectionRefusedError: # reachable but server.py is not running
        return {
            "host": host,
            "port": port,
            "success": False,
            "error": "connection refused"
        }

    except OSError as e: # other network related issues
        return {
            "host": host,
            "port": port, 
            "success": False,
            "error": str(e)
        }


def fan_out_query(pattern): # querying all machines concurrently and gathers the results together
    machines = load_machines(CONFIG_FILE) # get list of tuple of host, port from config file and function above
    results = []

    with ThreadPoolExecutor(max_workers=len(machines)) as executor: # 10 machines 10 threads. just to understand how many threads to run 
        futures = []
        for host, port in machines:
            future = executor.submit(query_machine, host, port, pattern) # basically runs task at a different desk and has a future ticket whenever called to give the result
            futures.append(future)

        for future in futures:
            result = future.result() # basically get the stored result 
            results.append(result)

    return results

def print_aggregated_results(results):
    total_matches = 0
    successful = 0
    failed = 0

    for result in results:
        if not result["success"]:
            print(f"{result['host']}:{result['port']} - Failed: {result['error']}") # failure message
            failed += 1
            continue


        print(f"{result['host']}:{result['port']} - {result['count']} matches") # success message

        for line in result["lines"]:
            print(f"    [{result['host']}] {line}")

        total_matches += result["count"] # no of lines
        successful += 1 # no of connections

    print(f"\n{successful} machines responded, {failed} failed")
    print(f"Total matches across all machines: {total_matches}")


if __name__ == "__main__":
    pattern = input("Enter a grep pattern: ")
    start_time = time.time()
    results = fan_out_query(pattern)
    time_taken = time.time() - start_time
    print_aggregated_results(results)
    print(f"Time taken: {time_taken:.2f} seconds")