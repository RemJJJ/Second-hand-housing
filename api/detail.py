from flask import Blueprint, request, Response, jsonify
from models import House
from sqlalchemy import func
from datetime import datetime, timedelta
import random
from utils.linear_model import linear_model_main

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

    # 先查询当前房源所在的街道信息
    current_house = House.query.filter(House.block == block).first()
    if not current_house:
        print(f"未找到小区 {block} 的房源信息")
        return jsonify({"code": 1, "msg": "未找到小区信息", "data": {}})

    current_region = current_house.region
    # print(f"当前房源所在街道: {current_region}")

    # 按街道查询该街道下各小区的房源数量统计，取前20
    result = (
        House.query.with_entities(House.block, func.count())
        .filter(House.region == current_region)  # 只查询同一街道的小区
        .group_by(House.block)
        .order_by(func.count().desc())
        .limit(20)  # 限制只显示前20个小区
        .all()
    )
    # print(f"查询结果: {result}")

    # 处理数据格式
    name_list_x = []
    num_list_y = []

    for item in result:
        name_list_x.append(item[0])
        num_list_y.append(item[1])

    data = {"name_list_x": name_list_x, "num_list_y": num_list_y}

    #  print(f"处理后的数据: {data}")
    return jsonify({"code": 0, "msg": "查询出来", "data": data})


# 房价预测 线性回归点状图
@detail_api.route("/scatterdata/<block>", methods=["post"])
def scatter_data(block):

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

    # 生成最近30天的日期列表  从数据库中获取所有房源的发布时间，并根据最新的房源生成最近30天的日期。
    date_list = []
    for i in range(1, 30):
        # 将时间戳(timestamp)转换成具体的日期
        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))
        # 获取最新房源发布时间的i天
        day = latest_release + timedelta(days=-i)
        # 将i天的日期格式化为字符串的形式并添加到date_list列表中
        # y = 年 m = 月 d = 日
        date_list.append(day.strftime("%m-%d"))
    # 将日期列表反转
    date_list.reverse()

    # 获取平均价格
    data = []
    x = []
    y = []

    # 将result结果转换为列表格式
    for index, i in enumerate(result):
        # 将平均价格的索引添加到x列表中
        x.append([index])
        # 将平均价格四舍五入保留两位小数添加到y列表中
        y.append(round(i[0], 2))
        # 将索引和平均价格添加到data列表中
        data.append([index, round(i[0], 2)])

    # 对未来一天的价格做预测
    # 预测的索引值
    predict_value = len(data)

    # 调用线性回归模型进行预测  通过调用外部的线性回归函数预测未来的房价。
    predict_outcome = linear_model_main(x, y, predict_value)

    # 将预测出来的房价四舍五入
    p_outcome = round(predict_outcome[0], 2)

    # 将预测的数据加入到data列表中
    data.append([predict_value, p_outcome])

    return jsonify(
        {
            "code": 0,
            "msg": "查询出来",
            "data": {"data-predict": data, "date_li": date_list},
        }
    )


# 户型价格走势
@detail_api.route("/brokenlinedata/<block>", methods=["post"])
def broken_line_data(block):
    # 获取房源时间序列
    time_stamp = (
        House.query.with_entities(House.publish_time).filter(House.block == block).all()
    )

    # 生成最近14天的日期列表
    date_list = []
    for i in range(1, 14):
        # 将时间戳(timestamp)转换成具体的日期
        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))

        # 获取最新房源发布时间的i天
        day = latest_release + timedelta(days=-i)
        # 将i天的日期格式化为字符串的形式并添加到date_list列表中
        # y = 年 m = 月 d = 日
        date_list.append(day.strftime("%m-%d"))
    # 将日期列表反转
    date_list.reverse()

    roomdata1 = []

    # 1室1厅的户型   分别查询各个户型的平均房价/面积数据，并按时间顺序排列。
    rooms1 = (
        House.query.with_entities(func.avg(House.price / House.area))
        .filter(House.block == block, House.rooms == "1室1厅")
        .group_by(House.publish_time)
        .order_by(House.publish_time)
        .all()
    )

    for item in rooms1[-14:]:
        roomdata1.append(round(item[0], 2))

    roomdata2 = []
    # 2室1厅的户型
    rooms2 = (
        House.query.with_entities(func.avg(House.price / House.area))
        .filter(House.block == block, House.rooms == "2室1厅")
        .group_by(House.publish_time)
        .order_by(House.publish_time)
        .all()
    )

    for item in rooms2[-14:]:
        roomdata2.append(round(item[0], 2))

    roomdata3 = []
    # 2室2厅的户型
    rooms3 = (
        House.query.with_entities(func.avg(House.price / House.area))
        .filter(House.block == block, House.rooms == "2室2厅")
        .group_by(House.publish_time)
        .order_by(House.publish_time)
        .all()
    )

    for item in rooms3[-14:]:
        roomdata3.append(round(item[0], 2))

    roomdata4 = []
    # 3室2厅的户型
    rooms4 = (
        House.query.with_entities(func.avg(House.price / House.area))
        .filter(House.block == block, House.rooms == "3室2厅")
        .group_by(House.publish_time)
        .order_by(House.publish_time)
        .all()
    )

    for item in rooms4[-14:]:
        roomdata4.append(round(item[0], 2))

    return jsonify(
        {
            "code": 0,
            "msg": "查询出来",
            "data": {
                "1室1厅": roomdata1,
                "2室1厅": roomdata2,
                "2室2厅": roomdata3,
                "3室2厅": roomdata4,
                "date_li": date_list,
            },
        }
    )
