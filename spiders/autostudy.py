from feapder.db.mysqldb import MysqlDB
import study
import time

def autostudy_spider():
    token = ("eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6IjI0YzA5NmExLTNiY2UtNDEyMy05OTVmLWNjZjIzZDQ0ODg5YyIsInVzZXJJZCI6IjI4MDc0Y"
             "TI4LTE5MTItNDhhOC1hYmJjLTlmZmI1NjljZTdmYiIsImNsdXN0ZXJJZCI6InRjcHJvZCIsImV4cCI6MTczNjIyMTYwNH0.yOhpN4vc2xtTGHURp_qF5PBoZLJlg38_gjQy3paWmAfo3KmvVm_KES1BiD_8zNA4ezb0ukBCvM-WbsqTJvRvvw")
    # 查询数据
    db = MysqlDB()
    sql = "SELECT * FROM detial_list"
    # sql = "SELECT * FROM `detial_list` WHERE `type` > 5 ORDER BY `type` ASC"
    data = db.find(sql, limit=6)

    for row in data:
        if row[6] < 2 and row[7] <= 4:
            print(row[2])
            print(row[3])
            kngId = row[3]
            courseId = row[2]
            title = row[0]
            name = row[1]
            study.send_request_1(token)
            time.sleep(0.5)
            study.send_request_2_and_3(kngId, courseId, token, title, name)
        else:
            print(row[2])
            print(row[3])
            title = row[0]
            name = row[1]
            print(f"{title}{name}  已完成学习，跳过本课")



if __name__ == '__main__':
    autostudy_spider()


