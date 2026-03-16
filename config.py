# config.py - 配置文件
import os

# 数据库配置：使用项目根目录下的 blog.db 文件
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'