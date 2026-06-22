import dns.resolver
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

target_domain = input("Enter target domain: ")

found_subdomains = []

with open("wordlist.txt", "r") as file:
    subdomains = file.read().splitlines()


def check_subdomain(sub):
    domain = f"{sub}.{target_domain}"

    try:
        dns.resolver.resolve(domain, "A")
        print(f"[FOUND] {domain}")
        found_subdomains.append(domain)

    except:
        pass


print("\nStarting Enumeration...\n")

with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(check_subdomain, subdomains)

print("\nEnumeration Complete")
print(f"Total Found: {len(found_subdomains)}")

# TXT Report
with open("reports/results.txt", "w") as report:
    report.write(f"Target: {target_domain}\n")
    report.write(f"Scan Date: {datetime.now()}\n\n")

    for domain in found_subdomains:
        report.write(domain + "\n")

# HTML Report
html = f"""
<html>
<head>
<title>Subdomain Enumeration Report</title>
<style>
body {{
font-family: Arial;
margin: 20px;
}}
</style>
</head>
<body>

<h1>Subdomain Enumeration Report</h1>

<p><b>Target:</b> {target_domain}</p>
<p><b>Total Found:</b> {len(found_subdomains)}</p>

<ul>
"""

for domain in found_subdomains:
    html += f"<li>{domain}</li>"

html += """
</ul>
</body>
</html>
"""

with open("reports/results.html", "w") as file:
    file.write(html)

print("\nReports Generated Successfully!")
