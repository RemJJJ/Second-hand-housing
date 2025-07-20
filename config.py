import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import pymysql

# 加载环境变量
load_dotenv()

pymysql.install_as_MySQLdb()

# 创建实例对象
db = SQLAlchemy()


class Config:
    host = str(os.getenv("db_host"))
    username = str(os.getenv("db_username"))
    password = str(os.getenv("db_password"))
    database = str(os.getenv("db_database"))

    # 调试模式
    DEBUG = False
    # 指定数据库的链接地址
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{username}:{password}@{host}:3306/{database}"
    )
    # 关闭警告信息
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 设置连接池相关参数
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 3600  # 1小时后强制重连
