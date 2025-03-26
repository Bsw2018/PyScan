import os
import sys
import json
import requests
sys.path.append(os.path.abspath("./lib"))
from colors import *
from cvss import CVSS2, CVSS3

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
def query_nvd(cpe, api_key, cvss_v2_vector=None):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe}"
    if cvss_v2_vector:
        url += f"&cvssV2Metrics={cvss_v2_vector}"

    headers = {"apiKey": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        #print(json.dumps(response.json(), indent=4))  # Debug the response
        return response.json()
    else:
        print(f"Error querying NVD: {response.status_code} - {response.text}")
        return None
    
#
# Process and print CVE information for a specific software.
#
def process_cve_data(cve_data):
    if not cve_data or "vulnerabilities" not in cve_data or not cve_data.get("vulnerabilities", []):
        print(f"\n{GREEN}No Vulnerabilities Found!{RESET}\n")
        return

    vulnerabilities_count = len(cve_data.get("vulnerabilities", []))
    print(f"Vulnerabilities Identified: {CYAN}{vulnerabilities_count}{RESET}\n")

    for idx, item in enumerate(cve_data.get("vulnerabilities", []), start=1):
        cve_id = item.get("cve", {}).get("id", "N/A")
        description = item.get("cve", {}).get("descriptions", [])
        description_text = description[0]["value"] if description else "No description available."
        metrics = item.get("cve", {}).get("metrics", {})

        # Extract CVSS4.0 metrics
        cvss_4 = metrics.get("cvssMetricV4", [{}])[0]  # Correct case-sensitive key
        vector_4 = cvss_4.get("cvssData", {}).get("vectorString", None)
        base_score_4 = cvss_4.get("cvssData", {}).get("baseScore", "N/A")
        severity_4 = cvss_4.get("cvssData", {}).get("baseSeverity", "Unknown")

        # Extract CVSS3.1 metrics
        cvss_3_1 = metrics.get("cvssMetricV31", [{}])[0]
        vector_3_1 = cvss_3_1.get("cvssData", {}).get("vectorString", None)
        base_score_3_1 = cvss_3_1.get("cvssData", {}).get("baseScore", "N/A")
        severity_3_1 = cvss_3_1.get("cvssData", {}).get("baseSeverity", "Unknown")

        # Extract CVSS2 metrics only if CVSS3.1 and CVSS4.0 are not available
        cvss_2 = None
        vector_2 = None
        base_score_2 = "N/A"
        severity_2 = "Unknown"

        if not vector_4 and not vector_3_1:  # Only consider CVSS2 if CVSS4.0 and CVSS3.1 are missing
            cvss_2 = metrics.get("cvssMetricV2", [{}])[0]
            vector_2 = cvss_2.get("cvssData", {}).get("vectorString", None)
            base_score_2 = cvss_2.get("cvssData", {}).get("baseScore", "N/A")
            severity_2 = cvss_2.get("baseSeverity", "Unknown")

        # Print CVE details
        print(f"{RED}{idx}. CVE ID: {cve_id}{RESET}")

        if vector_4:
            # Color the severity based on the value of severity_4
            if severity_4 == "CRITICAL":
                print(f"Severity: {BRIGHT_MAGENTA}{severity_4}{RESET}\nScore: {base_score_4}")
            elif severity_4 == "HIGH":
                print(f"Severity: {BRIGHT_RED}{severity_4}{RESET}\nScore: {base_score_4}")
            elif severity_4 == "MEDIUM":
                print(f"Severity: {YELLOW}{severity_4}{RESET}\nScore: {base_score_4}")
            elif severity_4 == "LOW":
                print(f"Severity: {GREEN}{severity_4}{RESET}\nScore: {base_score_4}")
            else:
                print(f"Severity: {BRIGHT_YELLOW}{severity_4}\nScore: {base_score_4}{RESET}") 

        elif vector_3_1:
            # Color the severity based on the value of severity_3_1
            if severity_3_1 == "CRITICAL":
                print(f"Severity: {BRIGHT_MAGENTA}{severity_3_1}{RESET}\nScore: {base_score_3_1}")
            elif severity_3_1 == "HIGH":
                print(f"Severity: {BRIGHT_RED}{severity_3_1}{RESET}\nScore: {base_score_3_1}")
            elif severity_3_1 == "MEDIUM":
                print(f"Severity: {YELLOW}{severity_3_1}{RESET}\nScore: {base_score_3_1}")
            elif severity_3_1 == "LOW":
                print(f"Severity: {GREEN}{severity_3_1}{RESET}\nScore: {base_score_3_1}")
            else:
                print(f"Severity: {BRIGHT_YELLOW}{severity_3_1}\nScore: {base_score_3_1}{RESET}") 

        elif vector_2:
            # Color the severity based on the value of severity_2
            if severity_2 == "CRITICAL":
                print(f"Severity: {BRIGHT_MAGENTA}{severity_2}{RESET}\nScore: {base_score_2}")
            elif severity_2 == "HIGH":
                print(f"Severity: {BRIGHT_RED}{severity_2}{RESET}\nScore: {base_score_2}")
            elif severity_2 == "MEDIUM":
                print(f"Severity: {YELLOW}{severity_2}{RESET}\nScore: {base_score_2}")
            elif severity_2 == "LOW":
                print(f"Severity: {GREEN}{severity_2}{RESET}\nScore: {base_score_2}")
            else:
                print(f"Severity: {BRIGHT_YELLOW}{severity_2}\nScore: {base_score_2}{RESET}") 

        else:
            print("Severity: UNKNOWN")

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

        print(f"\nChecking {CYAN}{software_name} {software_version}{RESET} against NVD\n")
        cve_data = query_nvd(cpe, api_key)
        process_cve_data(cve_data)

def calculate_cvss_score(version, vector_string):
    # Version handling for different CVSS scores
    try:    
        if version == "CVSS2":
            cvss = CVSS2(vector_string)
        elif version == "CVSS3":
            cvss = CVSS3(vector_string)
        elif version == "CVSS4":  
            cvss = CVSS3(vector_string)  
        else:
            raise ValueError("Unsupported CVSS version")
        return cvss.base_score
    except Exception as e:
        print(f"Error calculating CVSS score for {version}: {e}")
        return "N/A"


def main():
    text = "BEGINNING NIST NVD QUERY MODULE"
    padding = 2 
    width = len(text) + (padding * 2)

    print(f"\n\n\t\t{BRIGHT_MAGENTA}╔" + "═" * width + "╗")
    print("\t\t║" + " " * width + "║")
    print(f"\t\t║{' ' * padding}{BRIGHT_CYAN}{text}{BRIGHT_MAGENTA}{' ' * padding}║")
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

    text = "NVD QUERY MODULE CLEAN EXIT"
    padding = 2 
    width = len(text) + (padding * 2)

    print(f"\n\n\t\t{BRIGHT_MAGENTA}╔" + "═" * width + "╗")
    print("\t\t║" + " " * width + "║")
    print(f"\t\t║{' ' * padding}{BRIGHT_CYAN}{text}{BRIGHT_MAGENTA}{' ' * padding}║")
    print("\t\t║" + " " * width + "║")
    print("\t\t╚" + "═" * width + "╝" + RESET + "\n\n")

# Remove upon final integration
if __name__ == "__main__":
    main()