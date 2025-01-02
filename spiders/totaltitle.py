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

        url = "https://api-phx-tc.yunxuetang.cn/kng/knowledge/pagelist"
        params = {
            "limit": "1",
            "offset": "0",
            "orderType": "desc",
            "orderBy": "createTime"
        }
        data = {
            "collegeId": "24c096a1-3bce-4123-995f-ccf23d44889c",
            "catalogId": "",
            "title": "",
            "type": "",
            "allTag": 1,
            "tagIds": []
        }
        data = json.dumps(data, separators=(',', ':'))
        yield feapder.Request(url, params=params, data=data, method="POST",callback=self.parse_count)

    def download_midware(self, request):
        token = ("eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6IjI0YzA5NmExLTNiY2UtNDEyMy05OTVmLWNjZjIzZDQ0ODg5YyIsInVzZXJJZCI6IjI4MD"
                 "c0YTI4LTE5MTItNDhhOC1hYmJjLTlmZmI1NjljZTdmYiIsImNsdXN0ZXJJZCI6InRjcHJvZCIsImV4cCI6MTczNjIyMTYwNH0.yOhpN4vc2xtTGHURp_qF5PBoZLJlg38_gjQy3paWmAfo3KmvVm_KES1BiD_8zNA4ezb0ukBCvM-WbsqTJvRvvw")
        request.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "access-key": "undefined",
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
            "token": token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-yxt-product": "xxv2",
            "yxt-orgdomain": "u.sdhsg.com",
            "yxtspanid": "d2849ba6f77bdd9d",
            "yxttraceid": "5.24c096a1-3bce-4123-995f-ccf23d44889c.28074a28-1912-48a8-abbc-9ffb569ce7fb.1735019893175.61183921"
        }
        return request
    #
    # def parse(self, request, response):
    #     # 确保调用的是真正的 response.json() 方法
    #     data = response.json  # 注意，这里是访问属性，而不是调用方法
    #     if callable(data):
    #         data = data()  # 如果 data 是一个方法，调用它
    #
    #     # 处理 JSON 数据
    #     print(data)

    def parse_count(self, request, response):
        # 确保获取的 JSON 数据正确
        count_data = response.json() if callable(response.json) else response.json
        # 解析 count
        count = count_data.get("paging", {}).get("count", 0)
        # count = 9
        print(f"Total count: {count}")
        url = "https://api-phx-tc.yunxuetang.cn/kng/knowledge/pagelist"
        params = {
            "limit": f"{count}",
            "offset": "0",
            "orderType": "desc",
            "orderBy": "createTime"
        }
        data = {
            "collegeId": "24c096a1-3bce-4123-995f-ccf23d44889c",
            "catalogId": "",
            "title": "",
            "type": "",
            "allTag": 1,
            "tagIds": []
        }
        data = json.dumps(data, separators=(',', ':'))
        yield feapder.Request(url, params=params, data=data, method="POST",callback=self.parse)

    def parse(self, request, response):
        response_json = response.json  # 获取 JSON 数据
        datas = response_json.get("datas", [])
        print(datas)

        # 数据入库
        for item in datas:
            title = item.get("title", "N/A")
            id = item.get("id", "N/A")
            studyScore = item.get("studyScore", "N/A")
            status  = item.get("status", "N/A")
            studyHours = item.get("studyHours", "N/A")
            type = item.get("type", "N/A")

            # 打印或者保存解析到的数据
            print(f"title: {title}, id: {id}, studyScore: {studyScore},status:{status},studyHours:{studyHours},type:{type}")


            item = total_list_item.TotalListItem()
            item.title = title
            item.Id = id
            item.studyScore = studyScore
            item.status = status
            item.studyHours =studyHours
            item.type = type
            yield item

if __name__ == "__main__":
    UrlSpider(redis_key="estudy:totallist").start()
