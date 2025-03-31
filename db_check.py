import nvdlib

# Search for vulnerabilities in OpenSSL

results = nvdlib.searchCVE(keywordSearch="openssl", limit=5)

for cve in results:
	print(f"CVE ID: {cve.id}")
	print(f"Description: {cve.descriptions[0].value}")
	print(f"Published Date: {cve.published}")
	print("-" * 40)