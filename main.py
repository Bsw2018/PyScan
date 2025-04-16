import sys
import os
import time
import threading
import subprocess
import report_gen




sys.path.append(os.path.abspath("./lib"))
from colors import *
from OsScanner.os_scan import OsScanner
from NetScanner.net_scan import NetScanner
from collections import OrderedDict


# A global timer that prints an updated elapsed time until told to stop.
def global_timer(stop_event, start_time, print_lock):
    while not stop_event.is_set():
        elapsed = int(time.time() - start_time)
        with print_lock:
            sys.stdout.write(f"\rTime Elapsed: {GREEN}{elapsed}{RESET}s")
        time.sleep(1)

# Runs a script and writes its output to a file.
def run_script(script_name, output_file, print_lock):
    start_time = time.time()
    module = script_name.replace('.py', '')
    # Execute the script via subprocess.
    with open(output_file, 'w', encoding='utf-8') as f:
        process = subprocess.Popen(
            ['python3', script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in process.stdout:
            f.write(line)
        for err_line in process.stderr:
            f.write(err_line)
    total_time = time.time() - start_time
    with print_lock:
        sys.stdout.write(f"\r{GREEN}{module}{RESET} finished. Total Time: {GREEN}{total_time:.2f}{RESET}s.")
        print()
        
# Creates and starts a thread for each module.
def run_modules(module_configs):
    threads = []
    report_files = {}
    print_lock = threading.Lock()  # To synchronize printing.

    # First, print all "executing" messages together.
    for module in module_configs:
        module_name = module["script"].replace('.py', '')
        with print_lock:
            print(f"Running {GREEN}{module_name}{RESET}:")
    
    # Start the global timer.
    global_start = time.time()
    timer_stop = threading.Event()
    timer_thread = threading.Thread(target=global_timer, args=(timer_stop, global_start, print_lock))
    timer_thread.start()

    # Now create and start a thread for each module.
    for module in module_configs:
        script = module["script"]
        output_file = module["output"]
        key = script.replace('.py', '')
        thread = threading.Thread(target=run_script, args=(script, output_file, print_lock))
        threads.append(thread)
        report_files[key] = output_file
        thread.start()

    # Wait for all module threads to complete.
    for t in threads:
        t.join()

    # Stop the global timer.
    timer_stop.set()
    timer_thread.join()
    
    return report_files

# Removes temporary output files.
def cleanup(report_files):
    for filename in report_files.values():
        try:
            os.remove(filename)
        except FileNotFoundError:
            print(f"File not found and could not be removed: {filename}")
        except Exception as e:
            print(f"Error removing file {filename}: {e}")

def main():
    scanner = OsScanner(output_file="system_info.json")
    scanner.get_installed_packages()
    scanner.output_system_metadata("os_meta_output.json")


    netscanner = NetScanner()
    netscanner.output_to_file("net_scan_output.json")



    modules = [
        {"script": "query_osv.py", "output": "osv_query_output.txt"},
        {"script": "query_nvd.py", "output": "nvd_query_output.txt"},
    ]
    
    # Run the modules concurrently.
    report_files_temp = run_modules(modules)
    
    
    report_files = OrderedDict()
    report_files["os_scan"] = "os_meta_output.json"
    report_files["net_scan"] = "net_scan_output.json"
    report_files.update(report_files_temp)


    report_gen.create_html_report(report_files)

    cleanup(report_files)

if __name__ == "__main__":
    main()