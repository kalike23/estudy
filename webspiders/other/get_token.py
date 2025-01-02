import sys

def get_token(username, password):
    token = ("eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6IjI0YzA5NmExLTNiY2UtNDEyMy05OTVmLWNjZjIzZDQ0ODg5YyIsInVzZXJJZCI6IjI4MD"
             "c0YTI4LTE5MTItNDhhOC1hYmJjLTlmZmI1NjljZTdmYiIsImNsdXN0ZXJJZCI6InRjcHJvZCIsImV4cCI6MTczNjIyMTYwNH0.yOhpN4vc2xtTGHURp_qF5PBoZLJlg38_gjQy3paWmAfo3KmvVm_KES1BiD_8zNA4ezb0ukBCvM-WbsqTJvRvvw")
    # 这里是获取 token 的逻辑
    # 例如调用 API 或从数据库中查询
    if username == "1" and password == "1":
        return token
    else:
        raise ValueError("账号或密码错误")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python get_token.py <username> <password>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    try:
        token = get_token(username, password)
        print(token)  # 输出 token
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)