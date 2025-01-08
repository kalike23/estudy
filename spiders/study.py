import requests
import json
import time

def send_request_1(token):
    """发送请求1"""
    url_1 = "https://api-phx-tc.yunxuetang.cn/kng/study/del/studying"
    headers = {
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
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-yxt-product": "xxv2",
        "yxt-orgdomain": "u.sdhsg.com",
        "yxtspanid": "2d5cd2af9c5f7fa8",
        "yxttraceid": "5.24c096a1-3bce-4123-995f-ccf23d44889c.28074a28-1912-48a8-abbc-9ffb569ce7fb.1735012469318.58295093",
        "token": token
    }
    data = json.dumps({}, separators=(',', ':'))
    response = requests.post(url_1, headers=headers, data=data)
    print(response.text)

def send_request_2_and_3(kngId, courseId, token, title, name):
    """发送请求2和请求3"""
    url_2 = "https://api-phx-tc.yunxuetang.cn/kng/study/submit/second"
    headers = {
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
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-yxt-product": "xxv2",
        "yxt-orgdomain": "u.sdhsg.com",
        "yxtspanid": "2d5cd2af9c5f7fa8",
        "yxttraceid": "5.24c096a1-3bce-4123-995f-ccf23d44889c.28074a28-1912-48a8-abbc-9ffb569ce7fb.1735012469318.58295093",
        "token": token
    }
    second_values = [1, 300]  # 循环的second值

    for i in range(100):
        # 请求2
        data_2 = {
            "acqSecond": second_values[0],
            "actualSecond": 20,
            "speed": 1,
            # "kngId": "04705b90-9d2f-4220-8cf8-cb9f54d07fc0",
            "kngId": f"{kngId}",
            "courseId": f"{courseId}",
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
        response = requests.post(url_2, headers=headers, data=json.dumps(data_2, separators=(',', ':')))
        print(response.text)
        if response.status_code == 200:
            result = response.json()
            if result.get("schedule") == 100:
                print(f"{title}{name}  已学完. Stopping loop.")
                break
        time.sleep(1)

        # 请求3
        data_2["acqSecond"] = second_values[1]  # 修改 second 为300
        response = requests.post(url_2, headers=headers, data=json.dumps(data_2, separators=(',', ':')))
        print(response.text)
        if response.status_code == 200:
            result = response.json()
            if result.get("schedule") == 100:
                print(f"{title}{name}  已学完. Stopping loop.")
                break
        time.sleep(1)

if __name__ == "__main__":
    # send_request_1()
    # time.sleep(0.5)
    # send_request_2_and_3()
    pass