import requests
import json
import re

def get_ip(urls, ips):
    result = set()
    for url in urls:
        for ip in ips:
            try:
                response = requests.get(f'https://dns.google/resolve?type=1&edns_client_subnet={ip}&name={url}')
                data = json.loads(response.text)
                if 'Answer' in data:
                    for answer in data['Answer']:
                        match = re.findall(r'\d+\.\d+\.\d+\.\d+', answer['data'])
                        if match:
                            result.add(match[0])
            except Exception as e:
                print(f"Error occurred for {url} and {ip}: {e}")
    return list(result)

# 示例的网址列表
urls = ['aliyun.2096.us.kg','3.1818.pp.ua','hk2.921219.xyz','hk.921219.xyz','hk1.921219.xyz','aliyun-hk.lianaishi.pub','hk.corevie.awcode.cn','hk08.yscard.gq','hk05.yscard.gq','hk10.yscard.gq','hk11.yscard.gq','max.jillmax1227.eu.org','kr.moonriver.sbs']
# 示例的 IP 列表
ips = ['114.114.114.114', '1.0.1.0', '8.8.8.8', '223.5.5.5']

ip_info = get_ip(urls, ips)

# 将结果保存到文件
with open('new_ip.txt', 'w') as file:
    for ip in ip_info:
        file.write(ip + '\n')
