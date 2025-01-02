from flask import Flask, request, jsonify

app = Flask(__name__)

def get_token(username, password):
    # 硬编码的 Token 示例
    token = ("eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6IjI0YzA5NmExLTNiY2UtNDEyMy05OTVmLWNjZjIzZDQ0ODg5YyIsInVzZXJJZCI6IjI4MD"
             "c0YTI4LTE5MTItNDhhOC1hYmJjLTlmZmI1NjljZTdmYiIsImNsdXN0ZXJJZCI6InRjcHJvZCIsImV4cCI6MTczNjIyMTYwNH0.yOhpN4vc2xtTGHURp_qF5PBoZLJlg38_gjQy3paWmAfo3KmvVm_KES1BiD_8zNA4ezb0ukBCvM-WbsqTJvRvvw")
    if username == "1" and password == "1":
        return token
    else:
        raise ValueError("账号或密码错误")

@app.route('/get-token', methods=['POST'])
def get_token_route():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "账号和密码不能为空"}), 400

    try:
        token = get_token(username, password)
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "请求失败: " + str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)  # 运行在独立的端口
