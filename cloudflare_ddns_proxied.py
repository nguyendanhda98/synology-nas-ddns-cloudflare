#!/usr/bin/env python3
import sys
import requests
import json

BAD_PARAMS = "badauth: Missing parameters (zone‑id, API token, hostname)."
if len(sys.argv) < 4:
    print(BAD_PARAMS)
    sys.exit(1)

ZONE_ID = sys.argv[1] # username
API_TOKEN = sys.argv[2] # password
HOSTNAME = sys.argv[3] # hostname
IP = sys.argv[4] if len(sys.argv) > 4 else None

TTL = 1
PROXIED = True

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

def get_public_ip():
    try:
        resp = requests.get("https://api.ipify.org")
        resp.raise_for_status()
        return resp.text.strip()
    except Exception as e:
        print(f"badauth: Unable to get public IP – {e}")
        sys.exit(1)

def lookup_record_id(record_type):
    """Tra record ID từ Cloudflare API dựa theo tên và loại (A hoặc AAAA)."""
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
    params = {"name": HOSTNAME, "type": record_type}
    resp = requests.get(url, params=params, headers=HEADERS)
    if resp.status_code != 200:
        print(f"badauth: Error listing records – HTTP {resp.status_code}")
        sys.exit(1)
    obj = resp.json()
    if not obj.get("success"):
        print(f"badauth: DNS list failed – {obj.get('errors')}")
        sys.exit(1)
    res = obj.get("result", [])
    if not res:
        print("badauth: record not found")
        sys.exit(1)
    return res[0]["id"], res[0].get("content")

def update_record(record_id, new_ip, record_type):
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}"
    payload = {
        "type": record_type,
        "name": HOSTNAME,
        "content": new_ip,
        "ttl": TTL,
        "proxied": PROXIED,
    }
    resp = requests.patch(url, headers=HEADERS, data=json.dumps(payload))
    try:
        obj = resp.json()
    except json.JSONDecodeError:
        print("badauth: Invalid JSON response")
        sys.exit(1)
    if obj.get("success"):
        print("good")
        sys.exit(0)
    else:
        print(f"badauth: Update failed – {obj.get('errors')}")
        sys.exit(1)

# START
if not IP:
    IP = get_public_ip()

record_type = "AAAA" if ":" in IP else "A"
record_id, current_ip = lookup_record_id(record_type)

if current_ip == IP:
    print("nochg")
    sys.exit(0)

update_record(record_id, IP, record_type)
