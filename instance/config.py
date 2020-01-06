#! usr/bin/python3
# -*- coding: utf-8 -*-
"""
隐秘配置变量
"""

import os

SECRET_KEY = os.urandom(24)
TIMEZONE = 'Asia/Shanghai'
COMMAND_DIR = r'/usr/local/flask_houtai/flaskhoutai/env/bin'

# MySQL数据库
WOWRKSHEET = "zjx_worksheet"
WOWRKSHEET01 = "component_management"
WOWRKSHEET02 = "user_database"

# 数据库名称
DBNAME1 = 'component_management'
DBNAME2 = 'zjx_worksheet'

"""表名"""
TABLENAME1 = 'algorithmic_analysis'

"""表名"""
ME2_TABLENAME1 = 'worksheet_classification'
ME2_TABLENAME2 = 'worksheet_relation'
ME2_TABLENAME3 = 'origin_type'
ME2_TABLENAME4 = 'association_table_relation'

# Redis数据库

REDIS_HOST = "120.31.140.112"
REDIS_PORT = 6380
REDIS_PASSWORD = 'jcxt@123456'
REDIS_DB = 0
REDIS_DECODE_RESPONSES = 1
REDIS_ENCODING = 'utf-8'
REDIS_ENCODING_ERRORS = 'ignore'
REDIS_SOCKET_CONNECT_TIME = 1

# mongodb数据库
M_HOST = "120.31.140.112"
M_PORT = 27017
M_USER = "root"
M_PASSWORD = 'jcxt@123456'

M_DB = "admin"
M_DBNAME = "ex_infos"
M_DBNAME1 = "userconfig"
M_TABLENAME = "newinfos"

M_COLLECTION1 = "user_algorithmic_data"
M_COLLECTION2 = "algorithm_output"

# mysql连接池
DB_HOST = '120.31.140.112'
DB_PORT = 3306
DB_USER = 'f_user'
DB_PASS = 'jcxt@123456'
DB_POOL_MAX_CONN = 8

# 跳过token验证
tokenpath = ["/layout/shareurl/", "/layout/is_identifying/", "/databigscreen/shareurl/"]
# 基础角色id
roleid = "bc9359dc-1d1d-11e7-a8b1-ce19120e1336"

# celery
from kombu import Exchange
from kombu import Queue

BROKER_URL = 'redis://:{ps}@{host}:{port}/3'.format(ps=REDIS_PASSWORD, host=REDIS_HOST, port=REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://:{ps}@{host}:{port}/4'.format(ps=REDIS_PASSWORD, host=REDIS_HOST, port=REDIS_PORT)
CELERY_INCLUDE = ['tasks.tasks_general']
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_QUEUES = (
    Queue("tasks_general", Exchange("tasks_general"), routing_key="tasks_general"),
)

CELERY_ROUTES = {
    'tasks.tasks_general.*': {"queue": "tasks_general", 'exchange': "tasks_general", "routing_key": "tasks_general"},
}
CELERYD_MAX_TASKS_PER_CHILD = 10
CELERYBEAT_MAX_LOOP_INTERVAL = 10
CELERYBEAT_SYNC_EVERY = 0
CELERY_TRACE_APP = 1  # 生产环境关闭
CELERY_ENABLE_UTC = False

BEAT_DB = 'test'
beat_dburi = "mysql+pymysql://{ROOT}:{PASS}@{HOST}:{PORT}/{TABLE}".format(ROOT=DB_USER, PASS=DB_PASS,
                                                                          HOST=DB_HOST, PORT=DB_PORT,
                                                                          TABLE=BEAT_DB)
