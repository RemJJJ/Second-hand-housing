from flask import Flask, Blueprint, redirect, render_template
from flask import request
from models import User

user_page = Blueprint("user_page", __name__)


@user_page.route("/user")
@user_page.route("/user/<username>")
def index(username=None):
    # 获取cookie
    name = request.cookies.get("name")

    # 如果没有登录，重定向到首页
    if not name:
        return redirect("/")

    # 如果访问的是自己的页面
    if username is None or name == username:
        # 获取用户信息
        user = User.query.filter_by(name=name).first()
        if user:
            return render_template(
                "user.html",
                username=name,
                addr=user.addr if user.addr else "",
                email=user.email,
            )
        else:
            return render_template("user.html", username=name, addr="", email="")

    # 如果访问的是别人的页面，重定向到自己的页面
    else:
        return redirect(f"/user/{name}")
