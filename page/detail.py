from flask import Flask, Blueprint, render_template, redirect, url_for
from models import House
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

    return render_template("detail.html", house=house, recommend_li=recommend_houses)
