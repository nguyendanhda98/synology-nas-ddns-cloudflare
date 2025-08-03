1. SSH into Synology NAS:
Open a terminal on your computer and connect to your Synology NAS via SSH:
Make the script executable:
```
ssh admin@<NAS_IP>
```

2. Copy the Script to Synology NAS:
- Copy:
```
cp cloudflare_ddns.py /usr/syno/bin/ddns
```
```
cp cloudflare_ddns_proxied.py /usr/syno/bin/ddns
```
- Make the script executable:
```
sudo chmod +x /usr/syno/bin/ddns/cloudflare_ddns.py
```
```
sudo chmod +x /usr/syno/bin/ddns/cloudflare_ddns_proxied.py
```
3. Update Synology Configuration:

Edit /etc.defaults/ddns_provider.conf:
```
[Cloudflare]
    modulepath=/usr/syno/bin/ddns/cloudflare_ddns.py
    queryurl=https://api.cloudflare.com
[Cloudflare-Proxied]
    modulepath=/usr/syno/bin/ddns/cloudflare_ddns_proxied.py
    queryurl=https://api.cloudflare.com
```

How to edit:
```
vi /etc.defaults/ddns_provider.conf
```
`i` to use insert mode
`esc` to escape
`:x` to exit and save
`:x!` to force exit and save

4. Add DDNS in DSM (UI):

Go to Control Panel > External Access > DDNS.
Add a new entry:
Service Provider: Cloudflare
Hostname: <HOSTNAME> (example.com)
Username: <ZONE_ID> (Cloudflare Zone ID)
Password: <API_TOKEN> (Cloudflare API Token)