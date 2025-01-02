import requests


def check_score(token):
    """
    检查用户当前的学分
    :param token: 用户的 token
    :return: 当前学分
    """

    headers = {
        "accept": "application/json, text/plain, */*",
        "token": token
    }
    url = "https://api-phx-tc.yunxuetang.cn/ssp/score/top/user"
    params = {"type": "1", "userId": ""}

    response = requests.get(url, headers=headers, params=params)
    print(response.json())

if __name__ == '__main__':
    token = ("eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6IjI0YzA5NmExLTNiY2UtNDEyMy05OTVmLWNjZjIzZDQ0ODg5YyIsInVzZXJJZCI6IjI4MD"
             "c0YTI4LTE5MTItNDhhOC1hYmJjLTlmZmI1NjljZTdmYiIsImNsdXN0ZXJJZCI6InRjcHJvZCIsImV4cCI6MTczNjIyMTYwNH0.yOhpN4vc2xtTGHURp_qF5PBoZLJlg38_gjQy3paWmAfo3KmvVm_KES1BiD_8zNA4ezb0ukBCvM-WbsqTJvRvvw")
    check_score(token)