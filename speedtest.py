import requests
import time
import concurrent.futures
import logging
import random

# 配置日志记录
logging.basicConfig(level=logging.INFO)

# 定义读取 IP 地址的函数
def read_ips(file_path):
    with open(file_path, 'r') as file:
        ips = file.readlines()
    return [ip.strip() for ip in ips]

file_path = 'new_ip.txt'  # 替换为实际的文件路径
ips = read_ips(file_path)

# 用于存储成功请求的 IP 及其延迟和成功次数信息
successful_ips_info = {}

# 定义线程执行的函数
def test_ip(ip):
    total_delay = 0
    success_count = 0
    test_times = 5  # 增加测试次数
    for _ in range(test_times):
        url = f"http://{ip}"
        headers = {
            "host":"www.cloudflare.com"
        }
        start_time = time.time()
        try: 
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                end_time = time.time()
                delay = end_time - start_time
                total_delay += delay
                success_count += 1
            else:
                logging.warning(f"IP: {ip} 响应状态码非 200: {response.status_code}")
        except requests.exceptions.RequestException as e:  # 捕获所有 requests 异常
            logging.error(f"IP: {ip} 请求出现异常: {e}")
        # 添加随机延迟，范围在 1 到 3 秒之间
        time.sleep(random.uniform(1, 2))
    average_delay = total_delay / test_times
    if success_count >= 8:  # 设定一个较高的成功次数阈值
        successful_ips_info[ip] = (average_delay, success_count)

# 创建线程池
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # 调整线程数量
    futures = [executor.submit(test_ip, ip) for ip in ips]
    for future in concurrent.futures.as_completed(futures):
        try:
            pass
        except Exception as e:
            logging.error(f"任务执行出错: {e}")

# 筛选出满足成功次数要求的 IP 并排序
filtered_ips = [(ip, info[0]) for ip, info in successful_ips_info.items() if info[1] >= 8]
filtered_ips.sort(key=lambda x: x[1])

# 将排序后的结果写入 final_ip.txt
with open('final_ip.txt', 'w', encoding="utf-8") as file:
    for ip, delay in filtered_ips:
        file.write(f"{ip}, 平均延迟: {delay} 秒, 成功次数: {successful_ips_info[ip][1]}\n")