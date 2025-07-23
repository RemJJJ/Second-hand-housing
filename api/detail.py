from flask import Blueprint, request, Response, jsonify
from models import House
from sqlalchemy import func

detail_api = Blueprint("detail_api", __name__)


# 户型占比，饼图
@detail_api.route("/piedata/<block>", methods=["post"])
def pie_data(block):
    # print(f"接收到饼图数据请求，小区: {block}")

    # 按房型统计分组，倒序排序
    result = (
        House.query.with_entities(House.rooms, func.count())
        .filter(House.block == block)
        .group_by(House.rooms)
        .order_by(func.count().desc())
        .all()
    )
    # print(f"查询结果: {result}")

    data = []
    for item in result:
        data.append({"name": item[0], "value": item[1]})

    # print(f"处理后的数据: {data}")
    return jsonify({"code": 0, "msg": "查询出来", "data": data})


# 小区房源数量TOP20，柱状图
@detail_api.route("/columndata/<block>", methods=["post"])
def column_data(block):
    # print(f"接收到柱状图数据请求，小区: {block}")

    # 按小区统计房源数量，取TOP20
    result = (
        House.query.with_entities(House.block, func.count())
        .group_by(House.block)
        .order_by(func.count().desc())
        .limit(20)
        .all()
    )
    # print(f"查询结果: {result}")

    name_list_x = []
    num_list_y = []

    for item in result:
        name_list_x.append(item[0])
        num_list_y.append(item[1])

    data = {"name_list_x": name_list_x, "num_list_y": num_list_y}

    # print(f"处理后的数据: {data}")
    return jsonify({"code": 0, "msg": "查询出来", "data": data})
