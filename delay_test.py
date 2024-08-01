import socket
import time
import threading



# 定义读取 IP 地址的函数
def read_ips(file_path):
    with open(file_path, 'r') as file:
        ips = file.readlines()
    return [ip.strip() for ip in ips]


file_path = 'ok_ip.txt'  # 替换为实际的文件路径
ips = read_ips(file_path)

# 定义一个全局变量来存储线程结果
thread_results = {}

def measure_tcp_latency(ip, port, dns, index):
    try:
        # 创建套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间（例如 5 秒）
        sock.settimeout(5)
        start_time = time.time()
        sock.connect((ip, port))
        end_time = time.time()
        # 计算延迟
        latency = (end_time - start_time) * 1000
        sock.close()
        if latency <= 100:  # 只保留 100ms 以内的结果
            thread_results[index] = latency
    except Exception as e:
        thread_results[index] = None
# 示例 IP 数组
custom_port = 8443  # 自定义端口
dns = "223.5.5.5"

threads = []
for index, ip in enumerate(ips):
    thread = threading.Thread(target=measure_tcp_latency, args=(ip, custom_port, dns, index))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

# # 打印结果
# for index, latency in thread_results.items():
#     if latency is not None:
#         print(f"TCP latency for {ips[index]}:{custom_port} using {dns} is {latency} ms")
#     else:
#         print(f"Timeout or error occurred for {ips[index]}")
        
with open('final_ip.txt', 'w', encoding="utf-8") as file:
    for index, latency in thread_results.items():
        if latency is not None:
            print(f"TCP latency for {ips[index]}:{custom_port} using {dns} is {latency} ms")
            file.write(f"{ips[index]}\n")
        else:
            print(f"Timeout or error occurred for {ips[index]}")
        
