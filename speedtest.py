import requests
import time
import concurrent.futures

# 定义读取 IP 地址的函数
def read_ips(file_path):
    with open(file_path, 'r') as file:
        ips = file.readlines()
    return [ip.strip() for ip in ips]

# 定义测试 IP 的函数，增加重试机制
def test_ip(ip):
    url = f"http://{ip}"
    headers = {
        "host":"www.cloudflare.com"
    }
    start_time = time.time()
    print(f"{ip}：请求开始时间:", time.strftime("%y-%m-%d %H:%M:%S", time.localtime())) 
    retry_times = 3  # 设置重试次数
    timeout = 5  # 调整超时时间为 5 秒
    for _ in range(retry_times):
        try: 
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                end_time = time.time()
                delay = end_time - start_time
                return (ip, delay)
        except requests.exceptions.ConnectionError as e:
            print(f"连接异常，重试: {ip} - {e}")
        except requests.exceptions.Timeout as e:
            print(f"超时异常，重试: {ip} - {e}")
        except requests.exceptions.RequestException as e:
            print(f"其他请求异常，重试: {ip} - {e}")
    return None

file_path = 'new_ip.txt'  # 替换为实际的文件路径
ips = read_ips(file_path)

# 用于存储成功请求的 IP 及其延迟信息
successful_ips_with_delays = []

# 使用多线程
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(test_ip, ip) for ip in ips]
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            successful_ips_with_delays.append(result)

# 按照延迟从低到高排序
successful_ips_with_delays.sort(key=lambda x: x[1])

# 将排序后的结果写入 final_ip.txt
with open('final_ip.txt', 'w', encoding="utf-8") as file:
    for ip, delay in successful_ips_with_delays:
        file.write(f"{ip}, 延迟: {delay} 秒\n")
