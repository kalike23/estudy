# -*- coding: utf-8 -*-
"""
Created on 2024-12-26 14:51:58
---------
@summary:
---------
@author: Admin
"""

import feapder
from items import detial_list_item
from feapder.db.mysqldb import MysqlDB
import json
import time


class Study(feapder.Spider):
    # download_delay = 1  # 设置请求之间的延迟，单位为秒

    def start_requests(self):
        url_del = "https://api-phx-tc.yunxuetang.cn/kng/study/del/studying"
        del_data = {}

        # 发送删除请求
        request = feapder.Request(
            url_del,
            method="POST",
            headers=self.get_headers(),
            data=json.dumps(del_data),
            callback=self.second_requests
        )

        # 使用 download_midware 来处理请求头
        request = self.download_midware(request)

        yield request

    def second_requests(self, request, response):
        # 处理响应并发送第二请求
        print("Received response from delete request:", response.text)

        url = "https://api-phx-tc.yunxuetang.cn/kng/study/submit/second"
        params = {
            "trackId": ""
        }

        for i in range(1, 31):  # 假设你要发出 300 次请求
            # 通过取余操作交替使用 1 和 300
            second = 1 if i % 2 != 0 else 300

            data = {
                "acqSecond": second,
                "actualSecond": 20,
                "speed": 1,
                "kngId": "00f00b57-1c90-46ab-b2fb-f6f45b6e354f",
                "courseId": "",
                "viewLoc": 57,
                "targetId": "",
                "targetCode": "kng",
                "originOrgId": "",
                "targetParam": {
                    "taskId": "",
                    "projectId": "",
                    "flipId": "",
                    "batchId": ""
                }
            }
            data = json.dumps(data, separators=(',', ':'))
            request = feapder.Request(url, params=params, data=data, method="POST", headers=self.get_headers())

            # 使用 download_midware 来处理请求头
            request = self.download_midware(request)

            yield request
            time.sleep(1)  # 每个请求之间延迟 1 秒

    def get_headers(self):
        return {
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
            "token": "eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6IjI0YzA5NmExLTNiY2UtNDEyMy05OTVmLWNjZjIzZDQ0ODg5YyIsInVzZXJJZCI6IjI4MDc0YTI4LTE5MTItNDhhOC1hYmJjLTlmZmI1NjljZTdmYiIsImNsdXN0ZXJJZCI6InRjcHJvZCIsImV4cCI6MTczNjIyMTYwNH0.yOhpN4vc2xtTGHURp_qF5PBoZLJlg38_gjQy3paWmAfo3KmvVm_KES1BiD_8zNA4ezb0ukBCvM-WbsqTJvRvvw",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-yxt-product": "xxv2",
            "yxt-orgdomain": "u.sdhsg.com",
            "yxtspanid": "f83cd82879cf337c",
            "yxttraceid": "5.24c096a1-3bce-4123-995f-ccf23d44889c.28074a28-1912-48a8-abbc-9ffb569ce7fb.1735017406019.60672130"
        }

    def download_midware(self, request):
        # 处理请求头
        request.headers = self.get_headers()
        return request

    def parse(self, request, response):
        print(response.text)
        print(response)

if __name__ == "__main__":
    Study(redis_key="estudy:studying").start()
