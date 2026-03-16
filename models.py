# models.py - 定义所有数据库模型
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# 先创建db对象，稍后在app.py中与app关联
db = SQLAlchemy()

# 定义文章模型
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 【新增】外键，指向 users 表的 id 列

    def __repr__(self):
        return f'<Article {self.title}>'

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # 指定数据库中表的名字，可写可不写，但写了好

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)  # 存储密码的哈希值，不是明文密码！

    # 建立与文章的关系：一个用户可以写多篇文章
    # `backref` 参数使得我们可以通过 article.author 访问文章的作者
    articles = db.relationship('Article', backref='author', lazy='dynamic')

    def set_password(self, password):
        """接收明文密码，计算哈希值并存储"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证传入的明文密码是否与存储的哈希值匹配"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'