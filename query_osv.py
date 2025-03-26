import os
import sys
import json
import requests
sys.path.append(os.path.abspath("./lib"))
from cvss import CVSS3, CVSS4
from colors import *

def load_system_info(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

def query_osv(package_name, ecosystem):
    url = "https://api.osv.dev/v1/query"
    headers = {"Content-Type": "application/json"}
    payload = {"package": {"name": package_name, "ecosystem": ecosystem}}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying OSV for {ecosystem}: {e}")
        return None

def process_vulnerability_data(vulnerability_data):
    if not vulnerability_data or "vulns" not in vulnerability_data:
        return []

    vulnerabilities = vulnerability_data["vulns"]
    results = []
    for vuln in vulnerabilities:
        vuln_id = vuln.get("id", "N/A")
        severity_score, severity_rating = get_severity_score(vuln)
        description = vuln.get("summary", "No description available.")
        results.append({
            "id": vuln_id,
            "severity": severity_rating,
            "score": severity_score,
            "description": description
        })
    return results

def process_installed_software(installed_software):
    ecosystems = ["PyPI", "Maven", "npm", "Go", "RubyGems", "NuGet", "Linux", "Debian", "Ubuntu"]

    for software in installed_software:
        software_name = software.get("name")
        software_version = software.get("version")

        if not software_name or not software_version:
            print(f"Skipping invalid entry: {software}")
            continue

        print(f"\nChecking {CYAN}{software_name} {software_version}{RESET} against OSV")

        all_vulnerabilities = []
        for ecosystem in ecosystems:
            print(f"Trying ecosystem: {ecosystem}...", end="\r")

            vulnerability_data = query_osv(software_name, ecosystem)
            vulnerabilities = process_vulnerability_data(vulnerability_data)
            all_vulnerabilities.extend(vulnerabilities)

            if vulnerabilities:
                break

        if all_vulnerabilities:
            print(f"\nVulnerabilities Identified: {BRIGHT_RED}{len(all_vulnerabilities)}{RESET}\n")
            for idx, vuln in enumerate(all_vulnerabilities, start=1):
                severity_color = get_severity_color(vuln['severity'])
                
                print(f"{RED}{idx}. OSV Vulnerability ID: {vuln['id']}{RESET}")
                print(f"Severity: {severity_color}{vuln['severity']}{RESET}")  
                print(f"Score: {vuln['score']}")  
                print(f"Description: {vuln['description']}")
                print("-" * 50)
        else:
            print(f"\n\n{GREEN}No vulnerabilities found for {software_name} {software_version} across all ecosystems.{RESET}\n")

def calculate_cvss_rating(cvss_vector):
    """
    Determine if the CVSS vector is CVSS3 or CVSS4 and calculate the score.
    Returns (numerical_score, severity_rating).
    """
    try:
        if cvss_vector.startswith("CVSS:3"):
            cvss = CVSS3(cvss_vector)
        elif cvss_vector.startswith("CVSS:4"):
            cvss = CVSS4(cvss_vector)
        else:
            return "UNKNOWN", "UNKNOWN"

        numerical_score = cvss.scores()[0]  # First score is Base Score

        if numerical_score >= 9.0:
            severity_rating = "CRITICAL"
        elif numerical_score >= 7.0:
            severity_rating = "HIGH"
        elif numerical_score >= 4.0:
            severity_rating = "MEDIUM"
        else:
            severity_rating = "LOW"

        return numerical_score, severity_rating

    except Exception as e:
        print(f"Error calculating CVSS score: {e}")
        return "UNKNOWN", "UNKNOWN"

def get_severity_score(vuln):
    """Extract and calculate the highest-priority CVSS score (CVSS4 > CVSS3 > CVSS2)."""
    try:
        severity_list = vuln.get("severity", [])
        cvss_vector = None

        # Prioritize CVSS4 over CVSS3, and CVSS3 over CVSS2
        for severity in severity_list:
            if severity.get("type") == "CVSS_V4":
                cvss_vector = severity.get("score")
                break  # Prioritize CVSS4, so stop searching
            elif severity.get("type") == "CVSS_V3" and not cvss_vector:
                cvss_vector = severity.get("score")
            elif severity.get("type") == "CVSS_V2" and not cvss_vector:
                cvss_vector = severity.get("score")

        if cvss_vector:
            return calculate_cvss_rating(cvss_vector)

        return "UNKNOWN", "UNKNOWN"

    except Exception as e:
        print(f"Error extracting severity score: {e}")
        return "UNKNOWN", "UNKNOWN"


def get_severity_color(severity_rating):
    severity_colors = {
        "LOW": GREEN,
        "MEDIUM": YELLOW,
        "HIGH": BRIGHT_RED,
        "CRITICAL": BRIGHT_MAGENTA,
        "UNKNOWN": RESET  
    }
    return severity_colors.get(severity_rating, RESET)

def main():
    text = "BEGINNING OSV QUERY MODULE"
    padding = 2 
    width = len(text) + (padding * 2)

    print(f"\n\n\t\t{BRIGHT_MAGENTA}╔" + "═" * width + "╗")
    print("\t\t║" + " " * width + "║")
    print(f"\t\t║{' ' * padding}{BRIGHT_CYAN}{text}{BRIGHT_MAGENTA}{' ' * padding}║")
    print("\t\t║" + " " * width + "║")
    print("\t\t╚" + "═" * width + "╝" + RESET + "\n\n")

    json_file = "system_info.json"
    system_info = load_system_info(json_file)
    if not system_info:
        return

    installed_software = system_info.get("installed_software", [])
    if not installed_software:
        print("No installed software found in the JSON file.")
        return

    print(f"Found {len(installed_software)} installed packages. Querying OSV...\n")
    process_installed_software(installed_software)

    text = "OSV QUERY MODULE CLEAN EXIT"
    padding = 2 
    width = len(text) + (padding * 2)

    print(f"\n\n\t\t{BRIGHT_MAGENTA}╔" + "═" * width + "╗")
    print("\t\t║" + " " * width + "║")
    print(f"\t\t║{' ' * padding}{BRIGHT_CYAN}{text}{BRIGHT_MAGENTA}{' ' * padding}║")
    print("\t\t║" + " " * width + "║")
    print("\t\t╚" + "═" * width + "╝" + RESET + "\n\n")
    
if __name__ == "__main__":
    main()
