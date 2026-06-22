import dns.resolver
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

domain = input("Enter target domain: ")

found = []

with open("wordlist.txt", "r") as file:
    subdomains = file.read().splitlines()

print("\nStarting Enumeration...\n")


def scan(subdomain):

    target = f"{subdomain}.{domain}"

    try:
        answers = dns.resolver.resolve(target, "A")

        for answer in answers:

            ip = answer.to_text()

            print(f"[FOUND] {target} --> {ip}")

            found.append((target, ip))

    except:
        pass


with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(scan, subdomains)

print("\nEnumeration Complete")
print(f"Total Found: {len(found)}")

# TXT Report

with open("reports/results.txt", "w") as report:

    report.write(f"Target Domain: {domain}\n")
    report.write(f"Date: {datetime.now()}\n\n")

    for subdomain, ip in found:
        report.write(f"{subdomain} --> {ip}\n")

# HTML Report

html = f"""
<html>
<head>
<title>Subdomain Enumeration Report</title>
</head>
<body>

<h1>Subdomain Enumeration Report</h1>

<p><b>Target:</b> {domain}</p>
<p><b>Total Found:</b> {len(found)}</p>

<table border="1" cellpadding="10">
<tr>
<th>Subdomain</th>
<th>IP Address</th>
</tr>
"""

for subdomain, ip in found:

    html += f"""
    <tr>
        <td>{subdomain}</td>
        <td>{ip}</td>
    </tr>
    """

html += """
</table>

</body>
</html>
"""

with open("reports/results.html", "w") as report:
    report.write(html)

print("\nReports Generated Successfully!")
