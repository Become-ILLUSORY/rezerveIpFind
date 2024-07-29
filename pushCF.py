import requests
import json

def update_cloudflare_dns(ips, subdomain, zone_id, api_token):
    # Cloudflare API endpoint
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    
    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    
    
    
    # Get existing DNS records
    response = requests.get(url, headers=headers)
    existing_records = json.loads(response.text)['result']



    # Find the record for the specified subdomain
    record_id = None
    for record in existing_records:
        if record['name'] == subdomain:
            record_id = record['id']
            break
    
    if record_id:
        # Update existing record
        update_url = f"{url}/{record_id}"
        data = {
            "type": "A",
            "name": subdomain,
            "content": ips[0],  # Use the first IP in the list
            "ttl": 1,  # Auto TTL
            "proxied": True
        }
        response = requests.put(update_url, headers=headers, json=data)
    else:
        # Create new record
        data = {
            "type": "A",
            "name": subdomain,
            "content": ips[0],  # Use the first IP in the list
            "ttl": 1,  # Auto TTL
            "proxied": True
        }
        response = requests.post(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"Successfully updated DNS record for {subdomain}")
    else:
        print(f"Failed to update DNS record. Status code: {response.status_code}")
        print(response.text)




def read_ips(file_path):
    with open(file_path, 'r') as file:
        ips = file.readlines()
    return [ip.strip() for ip in ips]

file_path = 'final_ip.txt'  # 替换为实际的文件路径
ips = read_ips(file_path)


subdomain = "bestip.zhangyykk.cloudns.org"
zone_id = "206a9f560928c1f5102d5f6597e396f9"
api_token = "PemkmL8qNGu4783W2BzMH00gbbTxrdq-mTGvdFfb"
update_cloudflare_dns(ips, subdomain, zone_id, api_token)    
    




 












