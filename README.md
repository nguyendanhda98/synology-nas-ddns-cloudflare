1. SSH into Synology NAS:
Open a terminal on your computer and connect to your Synology NAS via SSH:
Make the script executable:
```
ssh admin@<NAS_IP>
```

2. Copy the Script to Synology NAS:
- Before copying
```
chown root:root cloudflare_ddns.py
```
```
chown root:root cloudflare_ddns_proxied.py
```
- Make sure end of files are LF (Unix) format:
```
sed -i 's/\r$//' cloudflare_ddns_test.py
```
```
sed -i 's/\r$//' cloudflare_ddns_proxied_test.py
```
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
Hostname: <ZONE_ID> (Cloudflare Zone ID)
Username: <DOMAINS> (example1.com|example2.com)
Password: <API_TOKEN> (Cloudflare API Token)