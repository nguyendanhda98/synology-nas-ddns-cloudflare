#!/usr/bin/env python3
import sys
import requests
import json

# ---- Cấu hình mặc định ----
TTL = 1
PROXIED = False

# ---- Xử lý đối số đầu vào ----
if len(sys.argv) < 4:
    print("badauth: Missing parameters (zone_id, domains, api_token).")
    sys.exit(1)

DOMAINS = sys.argv[1].split("|") # username
API_TOKEN = sys.argv[2] # password
ZONE_ID = sys.argv[3] # hostname
IP = sys.argv[4] if len(sys.argv) > 4 else None

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

def get_public_ip():
    try:
        res = requests.get("https://api.ipify.org", timeout=10)
        res.raise_for_status()
        return res.text.strip()
    except Exception as e:
        print(f"badauth: Failed to get public IP – {e}")
        sys.exit(1)

def lookup_record(domain, record_type):
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
    params = {"name": domain, "type": record_type}
    res = requests.get(url, headers=HEADERS, params=params)
    try:
        obj = res.json()
    except:
        print(f"badauth: Invalid JSON when querying {domain}")
        sys.exit(1)
    if not obj.get("success") or not obj.get("result"):
        print(f"badauth: Record not found for {domain}")
        sys.exit(1)
    return obj["result"][0]["id"], obj["result"][0].get("content")

def update_record(domain, record_id, ip, record_type):
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}"
    payload = {
        "type": record_type,
        "name": domain,
        "content": ip,
        "ttl": TTL,
        "proxied": PROXIED,
    }
    res = requests.patch(url, headers=HEADERS, data=json.dumps(payload))
    try:
        obj = res.json()
    except:
        print(f"badauth: Invalid JSON when updating {domain}")
        sys.exit(1)
    if obj.get("success"):
        print(f"good: {domain} updated to {ip}")
    else:
        print(f"badauth: Failed to update {domain} – {obj.get('errors')}")

# ---- Bắt đầu chương trình ----
if not IP:
    IP = get_public_ip()

record_type = "AAAA" if ":" in IP else "A"

for domain in DOMAINS:
    domain = domain.strip()
    if not domain:
        continue
    record_id, current_ip = lookup_record(domain, record_type)
    if current_ip == IP:
        print(f"nochg: {domain} already has {IP}")
        continue
    update_record(domain, record_id, IP, record_type)
