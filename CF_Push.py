from cloudflare import Cloudflare
import os

api_token = os.getenv('api_token')

zone_id = os.getenv('zone_id')

subdomain = os.getenv('subdomain')

def read_ips(file_path):
    with open(file_path, 'r') as file:
        ips = file.readlines()
    return [ip.strip() for ip in ips]

file_path = 'final_ip.txt'  # 替换为实际的文件路径
ips = read_ips(file_path)


client = Cloudflare(api_token=api_token)
dns_records = client.dns.records.list(zone_id=zone_id)

for record in dns_records:
    if record.name == subdomain:
        client.dns.records.delete(zone_id=zone_id, dns_record_id=record.id)
        print(f"删除 {record.name} 记录 {record.content}")

for ip in ips:
    client.dns.records.create(
        zone_id=zone_id,
        name=subdomain,
        type='A',
        proxied=False,
        ttl=1,
        content=ip
    )
    print(f"添加 {subdomain} 记录 {ip}")
