from flask import Flask, Blueprint, redirect, render_template, jsonify
from flask import request
from models import User, House, Recommend, db

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
        collect = user.collect_id
        if collect:
            collect_id = collect.split(",")
        else:
            collect_id = []
        print(collect_id)

        if collect_id:
            # 使用case when来按照collect_id中的顺序排序，最近的收藏（后面插入的）在最前面
            order_case = db.case(
                {
                    house_id: len(collect_id) - 1 - index
                    for index, house_id in enumerate(collect_id)
                },
                value=House.id,
            )
            houses = (
                House.query.filter(House.id.in_(collect_id))
                .order_by(order_case.asc())
                .all()
            )
        else:
            houses = []

        # 查询浏览记录
        from models import Recommend

        browse_records = (
            Recommend.query.filter_by(user_id=user.id)
            .order_by(Recommend.id.desc())
            .all()
        )

        print(houses)

        if user:
            return render_template(
                "user.html",
                username=name,
                addr=user.addr if user.addr else "",
                email=user.email,
                houses=houses,
                browse_records=browse_records,
            )
        else:
            return render_template("user.html", username=name, addr="", email="")

    # 如果访问的是别人的页面，重定向到自己的页面
    else:
        return redirect(f"/user/{name}")


# 清空浏览记录
@user_page.route("/deletebrowserecord", methods=["post"])
def delete_browse_record():
    username = request.cookies.get("name")
    if not username:
        return jsonify({"code": 0, "msg": "请先登录"})

    # 先获取用户ID
    user = User.query.filter(User.name == username).first()
    if not user:
        return jsonify({"code": 0, "msg": "用户不存在"})

    # 根据用户ID删除浏览记录
    rec = Recommend.query.filter(Recommend.user_id == user.id).delete()
    db.session.commit()
    return jsonify({"code": 1, "msg": "清空浏览记录成功"})
