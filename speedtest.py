import requests
import time

# 定义读取 IP 地址的函数
def read_ips(file_path):
    with open(file_path, 'r') as file:
        ips = file.readlines()
    return [ip.strip() for ip in ips]

file_path = 'new_ip.txt'  # 替换为实际的文件路径
ips = read_ips(file_path)

# 用于存储成功请求的 IP 及其延迟信息
successful_ips_with_delays = []

for ip in ips:
    url = f"http://{ip}"
    headers = {
        "host":"www.cloudflare.com"
    }
    start_time = time.time()
    print(f"{ip}：请求开始时间:", time.strftime("%y-%m-%d %H:%M:%S", time.localtime())) 
    try: 
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            end_time = time.time()
            delay = end_time - start_time
            successful_ips_with_delays.append((ip, delay))
    except requests.exceptions.RequestException as e:  # 捕获所有 requests 异常
        print("请求出现异常:", e) 

# 按照延迟从低到高排序
successful_ips_with_delays.sort(key=lambda x: x[1])

# 将排序后的结果写入 final_ip.txt
with open('final_ip.txt', 'w',encoding="utf-8") as file:
    for ip, delay in successful_ips_with_delays:
        file.write(f"{ip}, 延迟: {delay} 秒\n")
