from flask import Blueprint, request, Response, jsonify
from models import House
from sqlalchemy import func

detail_api = Blueprint("detail_api", __name__)


# 户型占比，饼图
@detail_api.route("/piedata/<block>", methods=["post"])
def pie_data(block):
    print(f"接收到饼图数据请求，小区: {block}")

    # 按房型统计分组，倒序排序
    result = (
        House.query.with_entities(House.rooms, func.count())
        .filter(House.block == block)
        .group_by(House.rooms)
        .order_by(func.count().desc())
        .all()
    )
    print(f"查询结果: {result}")

    data = []
    for item in result:
        data.append({"name": item[0], "value": item[1]})

    print(f"处理后的数据: {data}")
    return jsonify({"code": 0, "msg": "查询出来", "data": data})
