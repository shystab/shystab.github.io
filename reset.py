# update_db.py - 更新数据库结构
from app import app
from models import db

with app.app_context():
    # 删除所有表（清空数据）
    db.drop_all()
    # 根据最新的模型创建所有表
    db.create_all()
    print("✅ 数据库已根据最新模型重建完成！（注意：所有旧数据已清空）")