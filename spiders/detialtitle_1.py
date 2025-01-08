import feapder
from items import detial1_list_item
from feapder.db.mysqldb import MysqlDB
from bs4 import BeautifulSoup  # 导入 BeautifulSoup 库用于清理 HTML 标签
import json
import time


class DetialSpider(feapder.Spider):
    def start_requests(self):
        url = "https://api-phx-tc.yunxuetang.cn/o2o/client/projects/1856184391439151105/tree"
        params = {
            "preview": "false"
        }
        yield feapder.Request(url, params=params, method="GET")

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
            "yxtspanid": "4d1ec1240686ce49",
            "yxttraceid": "5.24c096a1-3bce-4123-995f-ccf23d44889c.28074a28-1912-48a8-abbc-9ffb569ce7fb.1736179849583.19601756"
        }
        return request


    def parse(self, request, response):
        #数据入库
        # id_tuple = request.meta.get("id_tuple")
        datas = response.json  # 获取 JSON 数据
        datas = datas.get("datas", [])
        datas = datas[0].get("studentTaskBeans", [])
        id_count = sum(1 for item in datas if 'id' in item)
        # print(datas[0])
        for i in range(id_count):
            datas_ = datas[i].get("groupCourse", [])
            id_count_ = sum(1 for item in datas_ if 'id' in item)
            print(datas_)
            for j in range(id_count_):
                name = datas_[j].get("name", "N/A")
                id = datas_[j].get("targetId", "N/A")
                item = detial1_list_item.Detial1ListItem()
                item.name = name
                item.kngId = id
                yield item



if __name__ == "__main__":
    DetialSpider(redis_key="estudy:detiallist").start()
