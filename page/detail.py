from flask import Flask, Blueprint, render_template, redirect, url_for, request, jsonify
from models import House, User, db
from sqlalchemy import func
import random

detail_page = Blueprint("detail_page", __name__)


@detail_page.route("/house/<id>")
def index(id=None):
    if not id:
        return redirect(url_for("index_page.index"))

    house = House.query.filter_by(id=id).first()
    if not house:
        return redirect(url_for("index_page.index"))

    # 判断是否收藏
    is_collect = False
    user_id = request.cookies.get("name")
    if user_id:
        user = User.query.filter(User.name == user_id).first()
        if user:
            collect = user.collect_id
            if collect:
                collect_id = collect.split(",")
                if id in collect_id:
                    is_collect = True
    # 根据当前房子的地区推荐6条最新上传的房源信息
    recommend_houses = (
        House.query.filter(
            House.region == house.region, House.id != house.id  # 同地区  # 排除当前房源
        )
        .order_by(House.publish_time.desc())  # 按发布时间倒序排列，最新的在前
        .limit(6)
        .all()
    )

    # 如果同地区房源不足6条，补充其他地区的最新房源
    if len(recommend_houses) < 6:
        remaining_count = 6 - len(recommend_houses)
        additional_houses = (
            House.query.filter(
                House.region != house.region,  # 不同地区
                House.id != house.id,  # 排除当前房源
            )
            .order_by(House.publish_time.desc())  # 按发布时间倒序排列
            .limit(remaining_count)
            .all()
        )
        recommend_houses.extend(additional_houses)

    return render_template(
        "detail.html", house=house, recommend_li=recommend_houses, is_collect=is_collect
    )


@detail_page.route("/collection/", methods=["post"])
def collection():
    hid = request.form.get("hid")
    print(hid)

    # 获取cookie判断用户是否登录
    user_id = request.cookies.get("name")
    print(user_id)
    if not user_id:
        return jsonify({"code": 0, "msg": "请先登录"})

    # 判断是否收藏(user中的collect_id字段)
    user = User.query.filter(User.name == user_id).first()

    if user:
        collect = user.collect_id
        #  分割collect_id
        if collect:
            collect_id = collect.split(",")
        else:
            collect_id = []
        if hid in collect_id:
            collect_id.remove(hid)
            user.collect_id = ",".join(collect_id)
            db.session.commit()
            return jsonify({"code": 2, "msg": "取消收藏成功"})
        else:
            collect_id.append(hid)
            user.collect_id = ",".join(collect_id)
            db.session.commit()
            return jsonify({"code": 1, "msg": "收藏成功"})
    else:
        return jsonify({"code": 0, "msg": "请先登录"})
