import CloudFlare


def read_ips(file_path):
    with open(file_path, 'r') as file:
        ips = file.readlines()
    return [ip.strip() for ip in ips]

file_path = 'final_ip.txt'  # 替换为实际的文件路径
ips = read_ips(file_path)

def update_ips_to_cloudflare(ips, subdomain, email, api_key):
    cf = CloudFlare.CloudFlare(email=email, token=api_key)
    zone_id = None
    record_id = None


    # 获取zone_id
    zones = cf.zones.get(params={'name': subdomain.split('.')[0]})
    if zones:
        zone_id = zones[0]['id']

    if not zone_id:
        print("未找到该域名的zone_id，请检查域名是否正确")
        return

    # 获取record_id
    records = cf.zones.dns_records.get(zone_id, params={'name': subdomain})
    if records:
        record_id = records[0]['id']

    if not record_id:
        print("未找到该子域名的record_id，请检查子域名是否正确")
        return

    # 更新IP地址
    new_ips = ','.join(ips)
    result = cf.zones.dns_records.put(record_id, data={
        'type': 'A',
        'name': subdomain,
        'content': new_ips,
        'ttl': 120,
        'proxied': False
    })

    if result['success']:
        print(f"子域名 {subdomain} 的IP地址已更新为：{new_ips}")
    else:
        print(f"更新失败：{result['errors'][0]['message']}")

# 示例用法
subdomain = 'bestip.zhangyykk.cloudns.org'
email = '2781885401@qq.com'
api_key = 'PemkmL8qNGu4783W2BzMH00gbbTxrdq-mTGvdFfb'

update_ips_to_cloudflare(ips, subdomain, email, api_key)




