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

    # 根据当前房子的小区推荐6条房源信息
    recommend_houses = (
        House.query.filter(
            House.block == house.block, House.id != house.id  # 同小区  # 排除当前房源
        )
        .limit(6)
        .all()
    )

    # 如果同小区房源不足6条，补充同街道的其他房源
    if len(recommend_houses) < 6:
        remaining_count = 6 - len(recommend_houses)
        additional_houses = (
            House.query.filter(
                House.region == house.region,  # 同街道
                House.block != house.block,  # 不同小区
                House.id != house.id,  # 排除当前房源
            )
            .limit(remaining_count)
            .all()
        )
        recommend_houses.extend(additional_houses)

    # 如果还是不足6条，补充其他房源
    if len(recommend_houses) < 6:
        remaining_count = 6 - len(recommend_houses)
        other_houses = (
            House.query.filter(House.id != house.id)  # 排除当前房源
            .limit(remaining_count)
            .all()
        )
        recommend_houses.extend(other_houses)

    return render_template("detail.html", house=house, recommend_li=recommend_houses)
