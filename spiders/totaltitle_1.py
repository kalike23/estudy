# -*- coding: utf-8 -*-
"""
Created on 2024-12-20 08:56:43
---------
@summary:
---------
@author: Admin
"""
import time

import feapder
import json
from items import total_list_item
from feapder.db.mysqldb import MysqlDB

class UrlSpider(feapder.Spider):

    def start_requests(self):
        # 清空数据
        db = MysqlDB()
        sql = "DELETE FROM total_list"
        affected_rows = db.delete(sql)
        print(f"成功删除 {affected_rows} 行数据")

        url = "https://api-phx-tc.yunxuetang.cn/o2o/study/list/nocount"
        params = {
            "desc": "1",
            "orderType": "1",
            "category": "",
            "status": "2",
            "keyword": "",
            "showUnFinish": "0",
            "limit": "16",
            "offset": "0",
            "tagIds": ""
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
            "yxtspanid": "9e322b2cf342b6fe",
            "yxttraceid": "5.24c096a1-3bce-4123-995f-ccf23d44889c.28074a28-1912-48a8-abbc-9ffb569ce7fb.1736178547818.21621147"
        }
        return request

    def parse(self, request, response):
        response_json = response.json  # 获取 JSON 数据
        datas = response_json.get("datas", [])
        print(datas)

       # 数据入库
        for item in datas:
            title = item.get("name", "N/A")
            id = item.get("projectId", "N/A")
            # studyScore = item.get("studyScore", "N/A")
            status  = item.get("completeStatus", "N/A")
            # studyHours = item.get("studyHours", "N/A")
            type = item.get("type", "N/A")

            # 打印或者保存解析到的数据
            print(f"title: {title}, id: {id}, status:{status}, type:{type}")


            item = total_list_item.TotalListItem()
            item.title = title
            item.Id = id
            # item.studyScore = studyScore
            item.status = status
            # item.studyHours =studyHours
            item.type = type
            yield item

if __name__ == "__main__":
    UrlSpider(redis_key="estudy:totallist").start()
