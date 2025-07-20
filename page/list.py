from flask import Flask, Blueprint, render_template, request, jsonify
from models import House
from config import db

list_page = Blueprint("list_page", __name__)


@list_page.route("/list")
def index():
    # 获取搜索参数
    search_keyword = request.args.get("search", "").strip()
    search_type = request.args.get("type", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 10  # 每页显示10条

    if search_keyword:
        # 根据搜索类型进行不同的查询
        if search_type == "户型搜索":
            query = House.query.filter(House.rooms.like(f"%{search_keyword}%"))
        elif search_type == "地区搜索":
            query = House.query.filter(
                db.or_(
                    House.region.like(f"%{search_keyword}%"),
                    House.address.like(f"%{search_keyword}%"),
                    House.block.like(f"%{search_keyword}%"),
                )
            )
        else:
            # 默认搜索所有字段
            query = House.query.filter(
                db.or_(
                    House.address.like(f"%{search_keyword}%"),
                    House.block.like(f"%{search_keyword}%"),
                    House.region.like(f"%{search_keyword}%"),
                    House.title.like(f"%{search_keyword}%"),
                    House.rooms.like(f"%{search_keyword}%"),
                )
            )

        # 分页查询
        houses = query.offset((page - 1) * per_page).limit(per_page).all()
        total_count = query.count()
        page_title = f"搜索结果：{search_keyword}"
    else:
        # 获取所有房源（分页）
        houses = House.query.offset((page - 1) * per_page).limit(per_page).all()
        total_count = House.query.count()
        page_title = "所有房源"

    # 计算总页数
    total_pages = (total_count + per_page - 1) // per_page

    return render_template(
        "list.html",
        houses=houses,
        page_title=page_title,
        search_keyword=search_keyword,
        current_page=page,
        total_pages=total_pages,
        total_count=total_count,
        has_more=page < total_pages,
    )


@list_page.route("/load_more", methods=["POST"])
def load_more():
    """AJAX加载更多数据"""
    data = request.get_json()
    page = data.get("page", 1)
    search_keyword = data.get("search_keyword", "").strip()
    search_type = data.get("search_type", "").strip()
    per_page = 10

    if search_keyword:
        # 根据搜索类型进行不同的查询
        if search_type == "户型搜索":
            query = House.query.filter(House.rooms.like(f"%{search_keyword}%"))
        elif search_type == "地区搜索":
            query = House.query.filter(
                db.or_(
                    House.region.like(f"%{search_keyword}%"),
                    House.address.like(f"%{search_keyword}%"),
                    House.block.like(f"%{search_keyword}%"),
                )
            )
        else:
            # 默认搜索所有字段
            query = House.query.filter(
                db.or_(
                    House.address.like(f"%{search_keyword}%"),
                    House.block.like(f"%{search_keyword}%"),
                    House.region.like(f"%{search_keyword}%"),
                    House.title.like(f"%{search_keyword}%"),
                    House.rooms.like(f"%{search_keyword}%"),
                )
            )
    else:
        query = House.query

    # 分页查询
    houses = query.offset((page - 1) * per_page).limit(per_page).all()
    total_count = query.count()
    total_pages = (total_count + per_page - 1) // per_page

    # 转换为JSON格式
    houses_data = []
    for house in houses:
        houses_data.append(
            {
                "id": house.id,
                "title": house.title or "暂无标题",
                "address": house.address or "暂无地址",
                "area": house.area or "暂无",
                "rooms": house.rooms or "暂无",
                "direction": house.direction or "暂无",
                "traffic": house.traffic or "暂无",
                "price": house.price or "暂无",
                "page_views": house.page_views or 0,
            }
        )

    return jsonify(
        {
            "success": True,
            "houses": houses_data,
            "has_more": page < total_pages,
            "current_page": page,
            "total_pages": total_pages,
        }
    )
