import time
import b22  # 导入22.py模块

for _ in range(10):
    print(_)
    # b22.Study(redis_key="estudy:studying").start() # 调用22.py中的main函数
    b22.Study().start()
    time.sleep(2)  # 每次执行之间等待1秒

