from config import db


# user_info表的模型类
class User(db.Model):
    # 表名
    __tablename__ = "user_info"
    # 用户ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户名
    name = db.Column(db.String(100))
    # 密码
    password = db.Column(db.String(100))
    # 邮箱地址
    email = db.Column(db.String(100))
    # 用户住址
    addr = db.Column(db.String(100))
    # 收藏房源ID
    collect_id = db.Column(db.String(250))
    # 用户浏览记录
    seen_id = db.Column(db.String(250))

    # 重写repr方法
    def __repr__(self):
        return "User: %s, %s" % (self.name, self.id)


# house_info表的模型类
# 房源信息
class House(db.Model):
    # 表名
    __tablename__ = "house_info"
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 房源标题
    title = db.Column(db.String(100))
    # 房源户型
    rooms = db.Column(db.String(100))
    # 建筑面积
    area = db.Column(db.String(100))
    # 价格
    price = db.Column(db.String(100))
    # 房屋朝向
    direction = db.Column(db.String(100))
    # 租住类型
    rent_type = db.Column(db.String(100))
    # 地址
    region = db.Column(db.String(100))
    # 房源所在街道
    block = db.Column(db.String(100))
    # 房源所在小区
    address = db.Column(db.String(100))
    # 交通条件
    traffic = db.Column(db.String(100))
    # 发布信息
    publish_time = db.Column(db.Integer)
    # 配套设施
    facilities = db.Column(db.TEXT)
    # 房屋买卖优势条件
    highlights = db.Column(db.TEXT)
    # 地标建筑
    matching = db.Column(db.TEXT)
    # 公交路线
    travel = db.Column(db.TEXT)
    # 浏览数量
    page_views = db.Column(db.Integer)
    # 房东业主
    landlord = db.Column(db.String(30))
    # 房东联系电话
    phone_num = db.Column(db.String(100))
    # 房源数量
    house_num = db.Column(db.String(100))

    # 重写repr方法，方便查看对象输出内容
    def __repr__(self):
        return "House title: %s, ID: %s" % (self.title, self.id)


# house_recommend表的模型类
# 存储用户浏览记录
class Recommend(db.Model):
    # 表名
    __tablename__ = "house_recommend"
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 用户ID
    user_id = db.Column(db.Integer)
    # 房源ID
    house_id = db.Column(db.Integer)
    # 房源标题
    title = db.Column(db.String(100))
    # 房源所在小区
    address = db.Column(db.String(100))
    # 房源所在街道
    block = db.Column(db.String(100))
    # 浏览次数
    score = db.Column(db.Integer)
