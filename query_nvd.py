import json
import requests
from colors import *

#
# Load installed software information from a JSON file.
#
def load_system_info(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None
    
#    
# Query the NVD API for vulnerabilities using a CPE identifier.
#
def query_nvd(cpe, api_key):
    
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe}"
    #print(url)
    headers = {
        "apiKey": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error querying NVD: {response.status_code} - {response.text}")
        print(response.json())
        return None
    
#
# Process and print CVE information for a specific software.
#
def process_cve_data(cve_data):
    """Process and print CVE information with severity for a specific software."""
    if not cve_data or "vulnerabilities" not in cve_data or not cve_data.get("vulnerabilities", []):
        print(f"\n{GREEN}No Vulnerabilities Found!{RESET}\n")
        return

    # Count the number of vulnerabilities
    vulnerabilities_count = len(cve_data.get("vulnerabilities", []))
    print(f"Vulnerabilities Identified: {BRIGHT_BLUE}{vulnerabilities_count}{RESET}\n")

    # Enumerate through the CVEs and print them with numbering
    for idx, item in enumerate(cve_data.get("vulnerabilities", []), start=1):
        cve_id = item.get("cve", {}).get("id", "N/A")
        severity = item.get("cve", {}).get("metrics", {}).get("cvssMetricV2", [{}])[0].get("baseSeverity", "Unknown")
        description = item.get("cve", {}).get("descriptions", [])
        description_text = description[0]["value"] if description else "No description available."

        # Print each CVE with numbering
        print(f"{RED}{idx}. CVE ID: {cve_id}{RESET}")
        
        # Print severity in appropriate color
        if severity == "LOW":
            print(f"Severity: {GREEN}{severity}{RESET}")
        elif severity == "MEDIUM":
            print(f"Severity: {YELLOW}{severity}{RESET}")
        elif severity == "HIGH":
            print(f"Severity: {BRIGHT_RED}{severity}{RESET}")
        elif severity == "CRITICAL":
            print(f"Severity: {BRIGHT_MAGENTA}{severity}{RESET}")
        else:
            print(f"Severity: {severity}")
        
        print(f"Description: {description_text}")
        print("-" * 50)
    
    print('\n')

# 
# Iterate through installed software and query vulnerabilities. 
#
def process_installed_software(installed_software, api_key):
    
    for software in installed_software:
        software_name = software.get("name")
        software_version = software.get("version")
        cpe = software.get("cpe")

        if not cpe:
            print(f"Skipping invalid entry: {software}")
            continue

        print(f"\nChecking {BRIGHT_BLUE}{software_name} {software_version}{RESET}\n")
        cve_data = query_nvd(cpe, api_key)
        process_cve_data(cve_data)


def main():
    text = "BEGINNING NIST NVD QUERY MODULE"
    padding = 2 
    width = len(text) + (padding * 2)

    print(f"\n\n\t\t{BRIGHT_GREEN}╔" + "═" * width + "╗")
    print("\t\t║" + " " * width + "║")
    print(f"\t\t║{' ' * padding}{text}{' ' * padding}║")
    print("\t\t║" + " " * width + "║")
    print("\t\t╚" + "═" * width + "╝" + RESET + "\n\n")

    api_key = "b52f218b-3379-4c3d-92f7-7d8b81ca0389"

    # Load system info from JSON
    json_file = "system_info.json"
    system_info = load_system_info(json_file)
    if not system_info:
        return

    installed_software = system_info.get("installed_software", [])
    if not installed_software:
        print("No installed software found in the JSON file.")
        return

    print(f"Found {len(installed_software)} installed packages. Querying NVD...\n")
    process_installed_software(installed_software, api_key)

# Remove upon final integration
if __name__ == "__main__":
    main()