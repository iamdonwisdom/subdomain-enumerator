import dns.resolver
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

print("""
=========================================
  Subdomain Enumeration Tool v2.0
  Author: Ede Chidozie Philip
=========================================
""")

domain = input("Enter target domain: ")
scan_time = datetime.now()

found = {}

with open("wordlist.txt", "r") as file:
    subdomains = file.read().splitlines()

print(f"\nScan Started: {scan_time}")
print("\nStarting Enumeration...\n")

def scan(subdomain):
    target = f"{subdomain}.{domain}"

    try:
        answers = dns.resolver.resolve(target, "A")

        for answer in answers:
            ip = answer.to_text()

            print(f"[FOUND] {target} --> {ip}")

            if target not in found:
                found[target] = []

            found[target].append(ip)

    except Exception:
        pass


with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(scan, subdomains)

print("\nEnumeration Complete")
print(f"Total Found: {len(found)}")

# TXT Report
with open("reports/results.txt", "w") as report:
    report.write(f"Target Domain: {domain}\n")
    report.write(f"Scan Date: {scan_time}\n\n")

    for subdomain, ips in found.items():
        report.write(f"{subdomain} --> {', '.join(ips)}\n")

# CSV Report
with open("reports/results.csv", "w") as report:
    report.write("Subdomain,IP Address\n")

    for subdomain, ips in found.items():
        report.write(f"{subdomain}, {' | '.join(ips)}\n")

# HTML Report
html = f"""
<html>
<head>
<title>Subdomain Enumeration Report</title>

<style>
body {{
    font-family: Arial, sans-serif;
    margin: 30px;
    background-color: #f4f6f9;
}}

h1 {{
    color: #2c3e50;
    text-align: center;
}}

.report-info {{
    background: white;
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 20px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}}

table {{
    border-collapse: collapse;
    width: 100%;
    background: white;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}}

th {{
    background-color: #2c3e50;
    color: white;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}}

tr:nth-child(even) {{
    background-color: #f2f2f2;
}}

tr:hover {{
    background-color: #e8f4ff;
}}
</style>

</head>

<body>

<h1>Subdomain Enumeration Report</h1>

<div class="report-info">
    <p><strong>Target Domain:</strong> {domain}</p>
    <p><strong>Total Subdomains Found:</strong> {len(found)}</p>
    <p><strong>Scan Date:</strong> {scan_time}</p>
</div>

<table>
<tr>
<th>Subdomain</th>
<th>IP Address</th>
</tr>
"""

for subdomain, ips in found.items():
    html += f"""
<tr>
    <td>{subdomain}</td>
    <td>{', '.join(ips)}</td>
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
print("TXT Report : reports/results.txt")
print("CSV Report : reports/results.csv")
print("HTML Report: reports/results.html")
