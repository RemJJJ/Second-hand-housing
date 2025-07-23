from flask import Blueprint, request, Response, jsonify
from models import House
from sqlalchemy import func
from datetime import datetime, timedelta
import random

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


# 小区房源数量TOP20，柱状图
@detail_api.route("/columndata/<block>", methods=["post"])
def column_data(block):
    print(f"接收到柱状图数据请求，小区: {block}")

    # 先查询当前房源所在的街道信息
    current_house = House.query.filter(House.block == block).first()
    if not current_house:
        print(f"未找到小区 {block} 的房源信息")
        return jsonify({"code": 1, "msg": "未找到小区信息", "data": {}})

    current_region = current_house.region
    print(f"当前房源所在街道: {current_region}")

    # 按街道查询该街道下各小区的房源数量统计，取前20
    result = (
        House.query.with_entities(House.block, func.count())
        .filter(House.region == current_region)  # 只查询同一街道的小区
        .group_by(House.block)
        .order_by(func.count().desc())
        .limit(20)  # 限制只显示前20个小区
        .all()
    )
    print(f"查询结果: {result}")

    # 处理数据格式
    name_list_x = []
    num_list_y = []

    for item in result:
        name_list_x.append(item[0])
        num_list_y.append(item[1])

    data = {"name_list_x": name_list_x, "num_list_y": num_list_y}

    print(f"处理后的数据: {data}")
    return jsonify({"code": 0, "msg": "查询出来", "data": data})


# 价格走势图，折线图（近14天）
@detail_api.route("/pricedata/<block>", methods=["post"])
def price_data(block):
    print(f"接收到价格走势数据请求，小区: {block}")

    # 生成近14天的日期
    dates = []
    prices = []
    base_price = 8500  # 基础价格

    for i in range(14):
        date = datetime.now() - timedelta(days=13 - i)
        dates.append(date.strftime("%m-%d"))

        # 生成带有线性回归趋势的价格数据
        # 添加一些随机波动，但保持整体上升趋势
        trend = i * 50  # 线性增长趋势
        random_factor = random.randint(-100, 100)  # 随机波动
        price = base_price + trend + random_factor
        prices.append(int(price))

    data = {"name_list_x": dates, "price_list_y": prices}

    print(f"处理后的数据: {data}")
    return jsonify({"code": 0, "msg": "查询出来", "data": data})


# 户型价格走势图，折线图（近14天）
@detail_api.route("/roompricedata/<block>", methods=["post"])
def room_price_data(block):
    print(f"接收到户型价格走势数据请求，小区: {block}")

    # 生成近14天的日期
    date_li = []
    for i in range(14):
        date = datetime.now() - timedelta(days=13 - i)
        date_li.append(date.strftime("%m-%d"))

    # 为不同户型生成带有线性回归趋势的价格数据
    base_prices = {"3室2厅": 9500, "2室2厅": 8500, "2室1厅": 7500, "1室1厅": 6500}

    data = {"date_li": date_li}

    for room_type, base_price in base_prices.items():
        prices = []
        for i in range(14):
            # 生成带有线性回归趋势的价格数据
            trend = i * 40  # 线性增长趋势
            random_factor = random.randint(-80, 80)  # 随机波动
            price = base_price + trend + random_factor
            prices.append(int(price))
        data[room_type] = prices

    print(f"处理后的数据: {data}")
    return jsonify({"code": 0, "msg": "查询出来", "data": data})
