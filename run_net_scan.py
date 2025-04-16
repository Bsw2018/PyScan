# run_net_scan.py
from NetScanner.net_scan import NetScanner

if __name__ == "__main__":
    scanner = NetScanner()
    scanner.output_to_file("net_scan_output.json")
