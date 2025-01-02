from feapder.db.mysqldb import MysqlDB
from queue import Queue
import threading
import time
from study import StudyClient
import logging

# 配置日志文件和格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("autostudy_spider.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

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

def process_course(db, client, kngId, courseId, title, name):
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
    except Exception as e:
        logging.error(f"课程学习失败: {title} - {name}，错误信息: {str(e)}")

def autostudy_spider(token):
    """
    自动学习任务主函数
    """
    client = StudyClient(token)
    db = db_pool.get_connection()  # 从连接池获取数据库连接

    try:
        sql = "SELECT * FROM detial_list"
        data = db.find(sql, limit=10)

        for row in data:
            title = row[0]
            name = row[1]
            kngId = row[3]
            courseId = row[2]

            if is_course_pending(row):
                process_course(db, client, kngId, courseId, title, name)
            else:
                logging.info(f"课程已完成，跳过: {title} - {name}")
    except Exception as e:
        logging.error(f"自动学习任务出错: {str(e)}")
    finally:
        db_pool.release_connection(db)  # 释放数据库连接回池
