import sys
import os
import time
import threading
import subprocess
import report_gen
sys.path.append(os.path.abspath("./lib"))
from colors import *

#
# Displays a loading message with elapsed time and module name.
#
def loading_message(start_time, module_name, stop_event):
    sys.stdout.write(f"\nRunning {GREEN}{module_name}{RESET}:\n")
    while not stop_event.is_set():
        elapsed_time = int(time.time() - start_time)
        sys.stdout.write(f"\rTime Elapsed: {GREEN}{elapsed_time}{RESET}s")
        sys.stdout.flush()
        time.sleep(0.5)

#
# Runs the query script and writes formatted outputs to a file using a local time keeper.
#
def run_query(script_name, output_file):
    local_stop_event = threading.Event()  # Time Keeper
    start_time = time.time()
    module_name = script_name.replace('.py', '')

    loader_thread = threading.Thread(target=loading_message, args=(start_time, module_name, local_stop_event))
    loader_thread.start()

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            process = subprocess.Popen(
                ['python3', script_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for line in process.stdout: #Write the standard output.
                f.write(line)
            for err_line in process.stderr: #Write error output, if any.
                f.write(err_line)
    finally:
        local_stop_event.set()
        loader_thread.join()
    print(f"\r{module_name} finished. Total Time: {GREEN}{time.time() - start_time:.2f}{RESET}s       ")

#
# Runs all query scripts based on the 'main'' configuration.
#
def run_all_modules(module_configs):

    report_files = {}
    for module in module_configs:
        script = module["script"]
        output_file = module["output"]
        run_query(script, output_file)
        key = script.replace('.py', '')
        report_files[key] = output_file
    return report_files

#
# Removes the temporary .txt files used to generate the final HTML report.
#
def cleanup(report_files):
    for filename in report_files.values():
        try:
            os.remove(filename)
        except FileNotFoundError:
            print(f"File not found and could not be removed: {filename}")
        except Exception as e:
            print(f"Error removing file {filename}: {e}")

    # module_configs: list of dicts where each dict has:
    #     - 'script':   Name of the query script (e.g., 'query_osv.py')
    #     - 'output':   Filename to which output is written (e.g., 'osv_query_output.txt')
    # Returns a dictionary mapping each module's name to its output file.
def main():
    modules = [
        {"script": "query_osv.py", "output": "osv_query_output.txt"},
        {"script": "query_nvd.py", "output": "nvd_query_output.txt"},
    ]

    # Run all queries and collect the resulting output files.
    report_files = run_all_modules(modules)

    report_gen.create_html_report(report_files)

    cleanup(report_files)

if __name__ == "__main__":
    main()
