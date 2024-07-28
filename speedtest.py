import requests
import time
import concurrent.futures
from collections import defaultdict

# 定义读取 IP 地址的函数
def read_ips(file_path):
    with open(file_path, 'r') as file:
        ips = file.readlines()
    return [ip.strip() for ip in ips]

# 定义测试 IP 的函数，并记录成功和失败次数
def test_ip(ip, success_count, failure_count):
    url = f"http://{ip}"
    headers = {
        "host":"www.cloudflare.com"
    }
    retry_times = 3  # 设置重试次数
    timeout = 5  # 调整超时时间为 5 秒
    for _ in range(retry_times):
        try: 
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                success_count[ip] += 1
                return True
        except requests.exceptions.RequestException as e:
            failure_count[ip] += 1
    return False

file_path = 'new_ip.txt'  # 替换为实际的文件路径
ips = read_ips(file_path)

# 用于存储成功和失败次数
success_count = defaultdict(int)
failure_count = defaultdict(int)

# 使用多线程进行测试
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(test_ip, ip, success_count, failure_count) for ip in ips]
    for future in concurrent.futures.as_completed(futures):
        pass

# 计算成功率
success_rate = {ip: success_count[ip] / (success_count[ip] + failure_count[ip]) for ip in ips}

# 按照成功率降序排序
sorted_ips = sorted(success_rate.items(), key=lambda x: x[1], reverse=True)

# 筛选成功率高的 IP
threshold = 0.8  # 可根据实际需求调整阈值
filtered_ips = [ip for ip, rate in sorted_ips if rate >= threshold]

# 输出成功率高的 IP
with open('final_ip.txt', 'w', encoding="utf-8") as file:
    for ip in filtered_ips:

        file.write(f"{ip}\n")
