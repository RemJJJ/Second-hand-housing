from flask import Blueprint, request, Response, jsonify
import bcrypt
from models import User
from config import db, Config
import json

user_api = Blueprint("user_api", __name__)

# print(Config.host)
# print(Config.username)
# print(Config.password)
# print(Config.database)


@user_api.route("/register", methods=["post"])
def register():
    data = request.form
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return jsonify({"valid": 0, "msg": "请填写所有必填字段"})

    # 检查用户是否已经存在
    print("准备查询")
    result = User.query.filter(User.name == username).first()

    if not result:
        # 使用bcrypt哈希算法+盐值加密密码
        salt = bcrypt.gensalt()
        hashed_password_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
        hashed_password = hashed_password_bytes.decode("utf-8")

        # 创建用户对象
        user = User()
        user.name = username
        user.password = hashed_password
        user.email = email

        db.session.add(user)
        db.session.commit()

        print(f"成功插入用户: {username}")
        return jsonify({"valid": 1, "msg": username})
    else:
        return jsonify({"valid": 0, "msg": "该用户已被注册"})


@user_api.route("/login", methods=["post"])
def login():
    print("准备查询")
    data = request.form
    username = data.get("username")
    password = data.get("password")
    print(username, password)
    if not username or not password:
        return jsonify({"valid": 0, "msg": "请填写所有必填字段"})

    user = User.query.filter(User.name == username).first()

    if not user:
        return jsonify({"valid": 0, "msg": "用户名不存在!"})

    print("用户对象:", user)
    print("用户密码:", user.password)

    hashed_password = user.password

    if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        # 设置cookie
        response = jsonify({"valid": 1, "msg": username})
        # 设置cookie, 两天后过期
        response.set_cookie("name", username, 172800)
        return response
    else:
        return jsonify({"valid": 0, "msg": "密码错误!"})


@user_api.route("/logout", methods=["get"])
def logout():
    # 获取cookie
    name = request.cookies.get("name")
    if not name:
        # print("后端拿到请求")
        return jsonify({"valid": 0, "msg": "用户未登录"})

    # 删除cookie
    response = jsonify({"valid": 1, "msg": "退出成功"})
    response.delete_cookie("name")
    # print("后端拿到请求")

    return response


@user_api.route("/update_profile", methods=["post"])
def update_profile():
    data = request.form
    original_username = data.get("original_username")
    username = data.get("username")
    addr = data.get("addr")
    password = data.get("password")
    email = data.get("email")

    # 如果新用户名和原用户名不相同，则查询新用户名是否存在
    if original_username != username:
        user = User.query.filter(User.name == username).first()
        if user:
            return jsonify({"valid": 0, "msg": "新用户名已存在"})

    # 如果新用户名与原用户名相同，则更新用户信息
    original_user = User.query.filter(User.name == original_username).first()
    if not original_user:
        return jsonify({"valid": 0, "msg": "原用户名不存在"})
    # 更新用户信息
    if username:
        original_user.name = username
    if addr:
        original_user.addr = addr
    if email:
        original_user.email = email
    if password:
        # 使用bcrypt哈希算法+盐值加密密码
        salt = bcrypt.gensalt()
        hashed_password_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
        hashed_password = hashed_password_bytes.decode("utf-8")
        original_user.password = hashed_password
    db.session.commit()
    response = jsonify({"valid": 1, "msg": "更新成功"})
    # 删除原用户名cookie
    response.delete_cookie("name")
    # 设置新用户名cookie
    response.set_cookie("name", str(username), 172800)
    return response
