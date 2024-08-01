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
print('第一个执行完毕')

# 启动第二个脚本
subprocess.run(['python','speedtest.py'], check=True)
print('第二个执行完毕')

# 启动第三个脚本
subprocess.run(['python','delay_test.py'], check=True)
print('第三个执行完毕')


# 启动第四个脚本
subprocess.run(['python','CF_Push.py'], check=True)
print('第四个执行完毕')
