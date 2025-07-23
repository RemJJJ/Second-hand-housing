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

    # 根据时间序列获取房源数据  House.price / House.area = 房子价格/房子面积
    result = (
        House.query.with_entities(func.avg(House.price / House.area))
        .filter(House.block == block)
        .group_by(House.publish_time)
        .order_by(House.publish_time)
        .all()
    )

    time_stamp = (
        House.query.with_entities(House.publish_time).filter(House.block == block).all()
    )
    time_stamp.sort(reverse=True)

    if not time_stamp:
        print(f"未找到小区 {block} 的时间戳数据")
        return jsonify({"code": 1, "msg": "未找到时间戳数据", "data": {}})

    # 生成最近14天的日期列表
    date_list = []
    for i in range(1, 15):
        # 将时间戳(timestamp)转换成具体的日期
        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))
        # 获取最新房源发布时间的i天
        day = latest_release + timedelta(days=-i)
        # 将i天的日期格式化为字符串的形式并添加到date_list列表中
        date_list.append(day.strftime("%m-%d"))
    # 将日期列表反转
    date_list.reverse()

    # 获取平均价格数据
    price_list = []
    for item in result[-14:]:  # 取最近14天的数据
        if item[0] is not None:
            price_list.append(round(item[0], 2))
        else:
            price_list.append(0)

    # 如果数据不足14天，用0填充
    while len(price_list) < 14:
        price_list.append(0)

    data = {"name_list_x": date_list, "price_list_y": price_list}

    print(f"处理后的数据: {data}")
    return jsonify({"code": 0, "msg": "查询出来", "data": data})


# 户型价格走势图，折线图（近14天）
@detail_api.route("/roompricedata/<block>", methods=["post"])
def room_price_data(block):
    print(f"接收到户型价格走势数据请求，小区: {block}")

    # 获取房源时间序列
    time_stamp = (
        House.query.with_entities(House.publish_time).filter(House.block == block).all()
    )

    if not time_stamp:
        print(f"未找到小区 {block} 的时间戳数据")
        return jsonify({"code": 1, "msg": "未找到时间戳数据", "data": {}})

    # 生成最近14天的日期列表
    date_list = []
    for i in range(1, 15):
        # 将时间戳(timestamp)转换成具体的日期
        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))
        # 获取最新房源发布时间的i天
        day = latest_release + timedelta(days=-i)
        # 将i天的日期格式化为字符串的形式并添加到date_list列表中
        date_list.append(day.strftime("%m-%d"))
    # 将日期列表反转
    date_list.reverse()

    # 先获取该小区的实际户型数据（与饼图相同）
    room_types_result = (
        House.query.with_entities(House.rooms, func.count())
        .filter(House.block == block)
        .group_by(House.rooms)
        .order_by(func.count().desc())
        .all()
    )

    if not room_types_result:
        print(f"未找到小区 {block} 的户型数据")
        return jsonify({"code": 1, "msg": "未找到户型数据", "data": {}})

    # 获取实际存在的户型
    actual_room_types = [item[0] for item in room_types_result]
    print(f"实际户型: {actual_room_types}")

    data = {"date_li": date_list}

    # 为每个实际户型查询价格数据
    for room_type in actual_room_types:
        # 查询该户型的平均房价/面积数据，并按时间顺序排列
        rooms_data = (
            House.query.with_entities(func.avg(House.price / House.area))
            .filter(House.block == block, House.rooms == room_type)
            .group_by(House.publish_time)
            .order_by(House.publish_time)
            .all()
        )

        room_prices = []
        for item in rooms_data[-14:]:  # 取最近14天的数据
            if item[0] is not None:
                room_prices.append(round(item[0], 2))
            else:
                room_prices.append(0)

        # 如果数据不足14天，用0填充
        while len(room_prices) < 14:
            room_prices.append(0)

        data[room_type] = room_prices

    print(f"处理后的数据: {data}")
    return jsonify({"code": 0, "msg": "查询出来", "data": data})
