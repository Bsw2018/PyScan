import json
import requests
import time

# Load installed software information from a JSON file.
def load_system_info(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Query OSV.dev API for vulnerabilities of a specific package and version.
def query_osv(package_name, version):
    """
    Query the OSV.dev API for vulnerabilities of a specific package and version.
    """
    url = "https://api.osv.dev/v1/query"
    payload = {
    "package": {
        "name": package_name,
        "ecosystem": get_ecosystem(package_name)
    },
    "version": version
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error querying OSV.dev: {response.status_code} - {response.text}")
        return None

def get_ecosystem(package_name):
    ecosystem_map = {
        "log4j": "Maven",
        "openssl": "Debian",
        "nginx": "Debian",
        "apache struts": "Maven"
    }
    return ecosystem_map.get(package_name.lower(), "Debian")  # Default to "Debian" if unknown

# Process and print vulnerability details for a package.
def process_vulnerabilities(vulns, package_name):
    """
    Process and print vulnerability details for a package.
    """
    if not vulns or "vulns" not in vulns:
        print(f"No vulnerabilities found for {package_name}.")
        return

    for vuln in vulns["vulns"]:
        print(f"CVE ID: {vuln.get('id', 'N/A')}")
        print(f"Summary: {vuln.get('summary', 'N/A')}")
        print(f"Severity: {vuln.get('severity', 'N/A')}")

        # Affected ranges or versions
        affects = vuln.get("affects", {}).get("ranges", [])
        for affect in affects:
            print(f"  - Affected OS/Repo: {affect.get('repo', 'N/A')}")
            print(f"    Introduced: {affect.get('introduced', 'N/A')}")
            print(f"    Fixed: {affect.get('fixed', 'N/A')}")

        # References
        references = vuln.get("references", [])
        for ref in references:
            print(f"  - Mitigation/Reference: {ref.get('url', 'N/A')}")

        print("-" * 40)

def main():
    print("\n\nBEGINNING OSV.DEV QUERY MODULE\n\n")

    # Path to your JSON file
    json_file = "system_info.json"

    # Load system info from JSON
    try:
        system_info = load_system_info(json_file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    # Query OSV.dev
    print("Retrieving installed software...")
    installed_software = system_info.get("installed_software", [])

    if not installed_software:
        print("No installed software found in the JSON file.")
        return

    print(f"Found {len(installed_software)} installed packages. Querying OSV.dev...")
    for software in installed_software:
        package_name = software.get("name")
        version = software.get("version")

        if not package_name or not version:
            print(f"Skipping invalid entry: {software}")
            continue

        print(f"Checking {package_name} (version {version})...")
        vulns = query_osv(package_name, version)
        process_vulnerabilities(vulns, package_name)
    
    time.sleep(2)

# Run the main function
if __name__ == "__main__":
    main()