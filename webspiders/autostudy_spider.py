import requests
from feapder.db.mysqldb import MysqlDB
from queue import Queue
import time
from study import StudyClient
import logging
import sys

# 创建自定义的流处理器
class FlushStreamHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()  # 强制刷新

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("autostudy_spider.log", encoding='utf-8', mode='a'),
        FlushStreamHandler(sys.stdout)  # 确保实时输出到控制台
    ]
)

# 学分检查函数
def check_score(token):
    """
    检查用户当前的学分
    :param token: 用户的 token
    :return: 当前学分
    """
    headers = {
        "accept": "application/json, text/plain, */*",
        "source": "501",
        "token": token

    }
    url = "https://api-phx-tc.yunxuetang.cn/ssp/score/top/user"
    params = {"type": "1", "userId": ""}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        score = result.get("score", 0)
        logging.info(f"当前学分: {score}")
        if score >= 500:
            return True
    else:
        logging.error(f"学分查询失败: {response.text}")
        return 0

# 全局数据库连接池
class DatabasePool:
    def __init__(self, size=5):
        """
        初始化数据库连接池
        :param size: 连接池大小
        """
        self.pool = Queue(maxsize=size)
        for _ in range(size):
            self.pool.put(MysqlDB())

    def get_connection(self):
        """
        获取一个数据库连接
        """
        return self.pool.get()

    def release_connection(self, connection):
        """
        释放数据库连接回池
        """
        self.pool.put(connection)

# 连接池实例（全局）
db_pool = DatabasePool(size=5)

def is_course_pending(row):
    """
    检查课程是否需要学习
    """
    return row[6] < 2 and row[7] <= 4

def update_course_status(db, kngId):
    """
    更新课程学习状态
    """
    sql = f"UPDATE detial_list SET studyStatus = 2 WHERE kngId = '{kngId}'"
    db.update(sql)

def process_course(db, client, kngId, courseId, title, name, token):
    """
    执行单门课程的学习任务
    """
    try:
        logging.info(f"开始学习课程: {title} - {name}")
        client.send_request_1()
        time.sleep(0.5)
        client.send_request_2_and_3(kngId, courseId, title, name)
        logging.info(f"完成课程: {title} - {name}")
        update_course_status(db, kngId)

        # 每完成一节课程，检查学分
        # score = check_score(token)
        if check_score(token):
            logging.info("已完成本年度学习，任务终止。")
            return True  # 返回 True 表示任务终止

    except Exception as e:
        logging.error(f"课程学习失败: {title} - {name}，错误信息: {str(e)}")

    return False  # 返回 False 表示继续任务

def autostudy_spider(token):
    """
    自动学习任务主函数
    """
    # score = check_score(token)
    if check_score(token):
        logging.info("已完成本年度学习，任务终止。")
    else:
        client = StudyClient(token)
        db = db_pool.get_connection()  # 从连接池获取数据库连接

        try:
            sql = "SELECT * FROM detial_list"
            data = db.find(sql, limit=0)

            for row in data:
                title = row[0]
                name = row[1]
                kngId = row[3]
                courseId = row[2]

                if is_course_pending(row):
                    if process_course(db, client, kngId, courseId, title, name, token):
                        break  # 如果任务终止，退出循环
                else:
                    logging.info(f"课程已完成，跳过: {title} - {name}")
        except Exception as e:
            logging.error(f"自动学习任务出错: {str(e)}")
        finally:
            db_pool.release_connection(db)  # 释放数据库连接回池
