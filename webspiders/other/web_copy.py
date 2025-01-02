from flask import Flask, request, jsonify, render_template
import autostudy_spider

app = Flask(__name__)

# 将 get_token 函数直接整合进来
def get_token(username, password):
    token = ("eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6IjI0YzA5NmExLTNiY2UtNDEyMy05OTVmLWNjZjIzZDQ0ODg5YyIsInVzZXJJZCI6IjI4MD"
             "c0YTI4LTE5MTItNDhhOC1hYmJjLTlmZmI1NjljZTdmYiIsImNsdXN0ZXJJZCI6InRjcHJvZCIsImV4cCI6MTczNjIyMTYwNH0.yOhpN4vc2xtTGHURp_qF5PBoZLJlg38_gjQy3paWmAfo3KmvVm_KES1BiD_8zNA4ezb0ukBCvM-WbsqTJvRvvw")
    if username == "1" and password == "1":
        return token
    else:
        raise ValueError("账号或密码错误")

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "账号和密码不能为空"}), 400

    try:
        token = get_token(username, password)  # 调用整合后的函数
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "请求失败: " + str(e)}), 500

@app.route('/start-study', methods=['POST'])
def start_study():
    data = request.json
    token = data.get('token')

    if not token:
        return jsonify({"message": "未提供 token"}), 400

    try:
        autostudy_spider.autostudy_spider(token)
        return jsonify({"message": "学习任务已启动"}), 200
    except Exception as e:
        return jsonify({"message": "启动学习任务失败: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
