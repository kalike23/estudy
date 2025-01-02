from flask import Flask, request, jsonify, render_template
import subprocess
import autostudy_spider

app = Flask(__name__)

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
        result = subprocess.run(
            ["python", "get_token.py", username, password],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            token = result.stdout.strip()
            return jsonify({"token": token}), 200
        else:
            return jsonify({"message": "获取 token 失败: " + result.stderr}), 500
    except Exception as e:
        return jsonify({"message": "请求失败: " + str(e)}), 500

@app.route('/start-study', methods=['POST'])
def start_study():
    data = request.json
    token = data.get('token')

    if not token:
        return jsonify({"message": "未提供 token"}), 400

    # 启动学习任务
    try:
        # 调用 autostudy_spider 函数，启动学习任务
        autostudy_spider.autostudy_spider(token)
        return jsonify({"message": "学习任务已启动"}), 200
    except Exception as e:
        return jsonify({"message": "启动学习任务失败: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)