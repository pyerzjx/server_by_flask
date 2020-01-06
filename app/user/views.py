from flask import Blueprint, request, jsonify, g
from utils.db_utils import redis
from instance import config
from utils.token_utils import TokenMaker
import datetime
from utils.db_utils import mysqlpool
import base64
import json
from utils.json_helper import DateEncoder

user = Blueprint("user", __name__)


@user.route("/login/", methods=["POST"])
def login():
    """用户登录功能"""
    json_data = request.get_json()
    username = json_data.get("userName")
    password = json_data.get("password")

    # 通过用户表获取token 相关信息 并判断账号密码是否正确
    conn = mysqlpool.get_conn()
    with conn.swich_db(config.WOWRKSHEET01) as cursor:
        return_list = conn.query_one(
            "select * from {} where UserName=%s and Password=%s".format(config.TABLENAME16), [username, password])
        if return_list:
            # 生成token
            token = TokenMaker().generate_token(return_list["id"], datetime.datetime.now())
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip = request.remote_addr
            conn.update(
                "update {} set LastLoginTime=%s,loginIp=%s where UserName=%s and Password=%s".format(
                    config.TABLENAME16),
                [date_time, ip, username, password])
        else:
            return jsonify({
                "code": -1,
                "data": "账号或密码错误，请重新输入账号密码"})

        # 缓存用户信息
        redis_value = base64.b64encode(json.dumps(return_list, cls=DateEncoder).encode("utf-8"))
        redis.set(token, redis_value)
        redis.expire(token, config.TOKEN_LIVE_TIME)

        return jsonify({
            "code": 1,
            "msg": {"roleId": return_list["RoleID"], "token": token, "userId": return_list["id"],
                    "userName": username}
        })


@user.route("/queryUserByUserName/", methods=["POST"])
def queryUserByUserName():
    """登陆用户信息查询接口"""
    json_data = request.get_json()
    username = json_data["userName"]
    try:
        conn = mysqlpool.get_conn()
        with conn.swich_db(config.WOWRKSHEET01) as cursor:
            # 通过 roles_users表 查询用户关系的角色ID  一个用户可能关系多个角色
            rolesid = conn.query_all(
                "select a.roleid,b.RoleName from {tableA} as a LEFT JOIN {tableB} as b on a.roleid= b.id where a.username=%s".format(
                    tableA=config.TABLENAME19, tableB=config.TABLENAME17), [username])
            rolesid_list = []
            rolesname_list = []
            for i in rolesid:
                rolesid_list.append(i["roleid"])
                rolesname_list.append(i["RoleName"])
            user_msg = conn.query_one(
                "select a.id,a.DepartmentID,a.LastLoginTime,a.RealName,a.Mobile,a.Email,a.status,a.remark,a.loginIp,b.full_name,b.short_name from {tableA} as a LEFT JOIN {tableB} as b on a.DepartmentID = b.number where a.UserName=%s".format(
                    tableA=config.TABLENAME16, tableB=config.TABLENAME21), [username])
        # 匿名函数 if null 返回 ""
        ft = lambda x: "" if not x else x
        return_dic = {}
        return_dic["DepartmentID"] = user_msg["DepartmentID"]
        return_dic["Email"] = ft(user_msg["Email"])
        return_dic["LastLoginTime"] = user_msg["LastLoginTime"].strftime("%Y-%m-%d %H:%M:%S")
        return_dic["Mobile"] = ft(user_msg["Mobile"])
        return_dic["RealName"] = user_msg["RealName"]
        return_dic["RoleID"] = rolesid_list
        return_dic["RoleName"] = rolesname_list
        return_dic["UserName"] = username
        return_dic["full_name"] = user_msg["full_name"]
        return_dic["id"] = user_msg["id"]
        return_dic["loginIp"] = user_msg["loginIp"]
        return_dic["remark"] = ft(user_msg["remark"])
        return_dic["short_name"] = ft(user_msg["short_name"])
        return_dic["status"] = user_msg["status"]

    except Exception as e:
        raise e
    return jsonify({
        "code": 1,
        "data": {
            "page": 1,
            "rows": [return_dic],
            "total": 1
        }
    })


@user.route("/signout/", methods=["POST"])
def signout():
    """用户退出"""
    json_data = request.get_json()
    token = json_data.get("token")

    redis.delete(token)

    return jsonify({
        "code": 1,
        "data": "成功退出"
    })
