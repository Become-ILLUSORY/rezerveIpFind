import os
import subprocess

# 删除指定文件
try:
    os.remove('final_ip.txt')
    os.remove('new_ip.txt')
except FileNotFoundError:
    pass  # 如果文件不存在，忽略错误

# 启动第一个脚本
subprocess.run(['python', 'getIP.py'], check=True)

# 启动第二个脚本
subprocess.run(['python','speedtest.py'], check=True)


# 启动第三个脚本
subprocess.run(['python','pushCF.py'], check=True)
