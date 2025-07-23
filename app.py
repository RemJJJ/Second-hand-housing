from flask import Flask, render_template

# 首页
from page.index import index_page
from page.detail import detail_page
from page.user import user_page
from page.list import list_page
from api.detail import detail_api

from config import Config, db

# 用户API
from api.user import user_api


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# 设置过滤器
def deal_title_over(title):
    # 处理None和空值
    if not title:
        return "暂无标题"

    # 转换为字符串
    title_str = str(title)

    if len(title_str) > 12:
        return title_str[:12] + "..."
    return title_str


# 注册过滤器
app.jinja_env.filters["deal_title_over"] = deal_title_over

# 注册首页
app.register_blueprint(index_page, url_prefix="/")

# 详情页
app.register_blueprint(detail_page, url_prefix="/")

# 个人中心
app.register_blueprint(user_page, url_prefix="/")

# 列表
app.register_blueprint(list_page, url_prefix="/")

# 详情页API
app.register_blueprint(detail_api, url_prefix="/get/")

# 注册用户登录与注册接口
app.register_blueprint(user_api, url_prefix="/")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
