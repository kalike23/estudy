import feapder
from items import detial_list_item
from items import total_list_item
from feapder.db.mysqldb import MysqlDB
from bs4 import BeautifulSoup  # 导入 BeautifulSoup 库用于清理 HTML 标签
import json
import time


class DetialSpider(feapder.Spider):
    def start_requests(self):
        # 清空数据
        db = MysqlDB()
        sql = "DELETE FROM detial_list"
        affected_rows = db.delete(sql)
        print(f"成功删除 {affected_rows} 行数据")
        # time.sleep(10)

        # 从total_list数据表中读取所有 ID
        db = MysqlDB()
        sql = "SELECT * FROM total_list"
        ids = db.find(sql, limit=0)
        # print(ids)

        for id_tuple in ids:
            if id_tuple[3] < 2:
                print(id_tuple[1])
                id = id_tuple[1]
                url = "https://api-phx-tc.yunxuetang.cn/kng/study/tree"
                data = {
                    "courseId": f"{id}",
                    "studyParam": {
                        "originOrgId": "",
                        "previewType": 0
                    },
                    "targetCode": "kng",
                    "targetId": "",
                    "targetParam": {
                        "taskId": "",
                        "projectId": "",
                        "flipId": "",
                        "batchId": ""
                    },
                    "customFunctionCode": ""
                }
                data = json.dumps(data, separators=(',', ':'))
                yield feapder.Request(url, data=data, method="POST",meta={"id_tuple": id_tuple})

    def download_midware(self, request):
        request.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://u.sdhsg.com",
            "priority": "u=1, i",
            "referer": "https://u.sdhsg.com/",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "source": "501",
            "token": "eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6IjI0YzA5NmExLTNiY2UtNDEyMy05OTVmLWNjZjIzZDQ0ODg5YyIsInVzZXJJZCI6IjI4MDc0YTI4LTE5MTItNDhhOC1hYmJjLTlmZmI1NjljZTdmYiIsImNsdXN0ZXJJZCI6InRjcHJvZCIsImV4cCI6MTczNzM2MDYxMH0.L8hPQ4Q6Xfn4W8EEf8lgcA-P4u8xotwyll-AbAYr5Len_n530TrCAzhE3l4TWNT2AbO0QXjifnpottUGJ3vDBQ",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-yxt-product": "xxv2",
            "yxt-orgdomain": "u.sdhsg.com",
            "yxtspanid": "93eaf7e4a9a7b3a0",
            "yxttraceid": "5.24c096a1-3bce-4123-995f-ccf23d44889c.28074a28-1912-48a8-abbc-9ffb569ce7fb.1735099729856.33446869"
        }
        return request

    def parse(self, request, response):
        #数据入库
        id_tuple = request.meta.get("id_tuple")
        print(response)
        if response.status_code == 200:
            print(response.json)
            print(id_tuple[0])
            data = response.json
            if data[0].get('bizAtt', {}) is not None:
                id_count = sum(1 for item in data if 'id' in item)
                for i in range(id_count):
                    item = detial_list_item.DetialListItem()
                    item.name = data[i]['name']
                    item.title = id_tuple[0]
                    item.courseId = id_tuple[1]
                    item.kngId = data[i]['id']
                    item.studyHours = data[i].get('bizAtt', {}).get('studyHours')
                    # item.studyHours = data[i]['bizAtt'].get('studyHours') if data[i]['bizAtt'] is not None else None
                    item.studyScore = data[i].get('bizAtt', {}).get('studyScores')
                    item.studyStatus = data[i]['studyStatus']
                    item.type = data[i]['type']
                    yield item
            else:
                id_count = sum(1 for item in data if 'id' in item)
                print(f"{data[0].get('name', {})}有:{id_count}")
                for i in range(id_count):
                    print(i)
                    # print(f"ID 数量: {id_count}")
                    # print( data[i].get('child'))
                    data_cache = data[i].get('child')
                    id_count_cache = sum(1 for item_cache in data_cache if 'id' in item_cache)
                    print(id_count_cache)
                    for j in range(id_count_cache):
                        print(data_cache[j].get('name'))
                        item = detial_list_item.DetialListItem()
                        item.name = data_cache[j]['name']
                        item.title = id_tuple[0]
                        item.courseId = id_tuple[1]
                        item.kngId = data_cache[j]['id']
                        item.studyHours = data_cache[j].get('bizAtt', {}).get('studyHours')
                        # item.studyHours = data[i]['bizAtt'].get('studyHours') if data[i]['bizAtt'] is not None else None
                        item.studyScore = data_cache[j].get('bizAtt', {}).get('studyScores')
                        item.studyStatus = data_cache[j]['studyStatus']
                        item.type = data_cache[j]['type']
                        yield item
        else:
            # print(400)
            item = detial_list_item.DetialListItem()
            item.title = id_tuple[0]
            item.name = ""
            item.courseId = ""
            item.kngId = id_tuple[1]
            item.studyHours = id_tuple[4]
            item.studyScore = id_tuple[2]
            item.studyStatus = id_tuple[3]
            item.type = id_tuple[5]
            yield item


        # # 更新数据
        # data = {
        #     "detial_question": detail_description,
        #     "answer": answer_content,
        #     "answerdate": answer_date
        # }
        # condition = f"questionID = '{question_id}'"
        #
        # db = MysqlDB()
        # success = db.update_smart(table="data", data=data, condition=condition)
        #
        # if success:
        #     print(f"Data for questionID {question_id} updated successfully.")
        # else:
        #     print(f"Failed to update data for questionID {question_id}.")




if __name__ == "__main__":
    DetialSpider(redis_key="estudy:detiallist").start()
