import feapder
import json
import time


class AirSpiderDemo(feapder.AirSpider):
    def start_requests(self,request_sync=True):
        # 初始请求1
        url_1 = "https://api-phx-tc.yunxuetang.cn/kng/study/del/studying"
        data_1 = {}
        data_1 = json.dumps(data_1, separators=(',', ':'))
        yield feapder.Request(url_1, data=data_1, method="POST")
        time.sleep(1)

        # 循环发送2、3请求
        second_values = [1, 300]  # 循环的second值
        for i in range(10):
            # 发送2请求
            url_2 = "https://api-phx-tc.yunxuetang.cn/kng/study/submit/second"
            data_2 = {
                "acqSecond": second_values[0],  # 第一次使用second值为1
                "actualSecond": 20,
                "speed": 1,
                "kngId": "001aed09-efdf-497b-be55-e1929beef9ca",
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
            data_2 = json.dumps(data_2, separators=(',', ':'))
            yield feapder.Request(url_2, data=data_2, method="POST")
            time.sleep(1)

            # 发送3请求
            data_3 = json.loads(data_2)  # 将data_2解析回字典
            data_3["acqSecond"] = second_values[1]  # 第二次使用second值为300
            data_3 = json.dumps(data_3, separators=(',', ':'))
            yield feapder.Request(url_2, data=data_3, method="POST")
            time.sleep(1)

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
            "token": "eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6IjI0YzA5NmExLTNiY2UtNDEyMy05OTVmLWNjZjIzZDQ0ODg5YyIsInVzZXJJZCI6IjI4MDc0YTI4LTE5MTItNDhhOC1hYmJjLTlmZmI1NjljZTdmYiIsImNsdXN0ZXJJZCI6InRjcHJvZCIsImV4cCI6MTczNjIyMTYwNH0.yOhpN4vc2xtTGHURp_qF5PBoZLJlg38_gjQy3paWmAfo3KmvVm_KES1BiD_8zNA4ezb0ukBCvM-WbsqTJvRvvw",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-yxt-product": "xxv2",
            "yxt-orgdomain": "u.sdhsg.com",
            "yxtspanid": "2d5cd2af9c5f7fa8",
            "yxttraceid": "5.24c096a1-3bce-4123-995f-ccf23d44889c.28074a28-1912-48a8-abbc-9ffb569ce7fb.1735012469318.58295093"
        }
        return request

    def parse(self, request, response):
        print(response.text)
        print(response)


if __name__ == "__main__":
    Study(redis_key="estudy:studying").start()
