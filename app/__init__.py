#! usr/bin/python3

"""
初始化flask
"""

from flask import Flask
from utils.db_utils import redis
from utils.websocket_util import Sockets


def create_app():
    """创建app"""
    app = Flask(__name__, instance_relative_config=True)

    # 加载配置
    app.config.from_object('config.default')
    app.config.from_object('config.production')
    app.config.from_pyfile('config.py')

    # 加载socket
    sockets = Sockets(app)
    redis.init_app(app)

    # 接口返回乱码问题
    app.config['JSON_AS_ASCII'] = False

    # 注册增加算法的蓝图
    from app.user.views import user
    app.register_blueprint(user, url_prefix="/user")

    # 注册websocket蓝图
    from app.websocket_api.views import ws
    sockets.register_blueprint(ws, url_prefix="/websocket")

    # 注册测试模块蓝图
    from tests.test import apitest
    app.register_blueprint(apitest,url_prefix="/apitest")

    return app
