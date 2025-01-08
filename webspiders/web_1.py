from flask import Flask, request, jsonify, render_template
import logging
import autostudy_spider

# # 配置日志记录
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("web_1.log", encoding='utf-8'),
#         logging.StreamHandler()
#     ]
# )

# 初始化 Flask 应用
app = Flask(__name__)

# 禁用 Flask 的访问日志
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# 将 get_token 函数封装为独立模块
def get_token(username, password):
    """
    模拟获取用户 Token
    :param username: 用户名
    :param password: 密码
    :return: Token 字符串
    """
    token = ("eyJhbGciOiJIUzUxMiJ9.eyJvcmdJZCI6IjI0YzA5NmExLTNiY2UtNDEyMy05OTVmLWNjZjIzZDQ0ODg5YyIsInVzZXJJZCI6IjI4MDc0YTI4LTE5MTItNDhhOC1hYmJjLTlmZmI1NjljZTdmYiIsImNsdXN0ZXJJZCI6InRjcHJvZCIsImV4cCI6MTczNzM2MDYxMH0.L8hPQ4Q6Xfn4W8EEf8lgcA-P4u8xotwyll-AbAYr5Len_n530TrCAzhE3l4TWNT2AbO0QXjifnpottUGJ3vDBQ")
    if username == "1" and password == "1":
        logging.info("用户登录成功，生成 Token")
        return token
    else:
        logging.warning(f"用户登录失败: 账号={username}, 密码错误")
        raise ValueError("账号或密码错误")

@app.route('/')
def home():
    """
    返回登录页面
    """
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """
    用户登录接口
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logging.warning("登录请求失败，账号或密码为空")
        return jsonify({"message": "账号和密码不能为空"}), 400

    try:
        token = get_token(username, password)
        return jsonify({"token": token}), 200
    except ValueError as e:
        logging.warning(f"登录失败: {str(e)}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logging.error(f"登录请求异常: {str(e)}")
        return jsonify({"message": "请求失败: " + str(e)}), 500

@app.route('/start-study', methods=['POST'])
def start_study():
    data = request.json
    token = data.get('token')

    if not token:
        logging.warning("学习任务启动失败，未提供 Token")
        return jsonify({"message": "未提供 token"}), 400

    try:
        # 清空日志文件内容
        open('autostudy_spider.log', 'w').close()

        logging.info(f"收到学习任务启动请求，Token: {token}")
        autostudy_spider.autostudy_spider(token)
        logging.info("学习任务已完成")
        return jsonify({"message": "学习任务已完成"}), 200
    except Exception as e:
        logging.error(f"学习任务启动失败: {str(e)}")
        return jsonify({"message": "启动学习任务失败: " + str(e)}), 500

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    返回 autostudy_spider.log 的实时日志内容
    """
    try:
        with open("autostudy_spider.log", "r", encoding="utf-8") as file:
            logs = file.readlines()[-60:]  # 获取最新 50 行日志
        return jsonify({"logs": logs})
    except Exception as e:
        logging.error(f"读取日志失败: {str(e)}")
        return jsonify({"message": "无法读取日志: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
