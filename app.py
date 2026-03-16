# app.py - Flask 应用主入口
from flask import Flask, render_template, request, redirect, url_for # 导入Flask和render_template
from models import db  # 从即将创建的models.py导入db
import config         # 从即将创建的config.py导入配置
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from flask import flash 

app = Flask(__name__) # 创建Flask应用实例 app作为经理
# 加载配置
app.config.from_object(config)
# 将app与db关联
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)  # 将其绑定到我们的 Flask 应用
login_manager.login_view = 'login'  # 告诉系统，当需要登录而未登录时，应跳转到名为 ‘login’ 的路由（我们稍后创建）
login_manager.login_message = '请先登录以访问此页面。'
@login_manager.user_loader
def load_user(user_id):
    from models import User  # 在函数内导入，避免循环依赖
    # 它接收一个字符串形式的用户ID，返回对应的用户对象，如果未找到则返回None
    return User.query.get(int(user_id))
# 首页路由 (暂时只是一个占位符)
@app.route('/')
def index():
    from models import Article
    articles = Article.query.order_by(Article.created_at.desc()).all()
    print(f"✅ 查询到了 {len(articles)} 篇文章")
    # 只需传递 articles，current_user 会自动由 Flask-Login 注入到模板上下文中
    return render_template('index.html', articles=articles)

@app.route('/admin/new', methods=['GET', 'POST'])
@login_required 
def new_article():
    """处理‘写新文章’页面：GET请求显示表单，POST请求保存数据"""
    from models import Article  # 在函数内导入，避免循环依赖
    if request.method == 'POST':
        # 1. 从表单中获取用户提交的数据
        title = request.form['title']
        content = request.form['content']
        # 2. 创建文章对象并保存到数据库
        print(f"DEBUG: current_user 类型: {type(current_user)}, 是否认证: {current_user.is_authenticated}") 
        if not current_user.is_authenticated:
            flash('请先登录再发表文章。')
            return redirect(url_for('login'))
        article = Article(title=title, content=content)
        article.author = current_user  # 【关键】关联当前用户
        db.session.add(article)
        db.session.commit()
        # 3. 保存成功后，重定向回首页（可以看到新文章）
        return redirect(url_for('index'))
    # 如果不是POST请求（即GET请求），则显示空表单页面
    return render_template('admin/new.html')
@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    """编辑指定ID的文章"""
    from models import Article
    # 首先，根据URL中的article_id从数据库获取要编辑的文章对象
    article = Article.query.get_or_404(article_id)

    if request.method == 'POST':
        # 处理表单提交：用新数据更新文章对象
        article.title = request.form['title']
        article.content = request.form['content']
        # 提交到数据库
        db.session.commit()
        # 成功后跳转回首页
        return redirect(url_for('index'))

    # 如果是GET请求，则显示一个预填了旧数据的表单
    return render_template('admin/edit.html', article=article)
@app.route('/login', methods=['GET', 'POST'])
def login():
    """处理用户登录"""
    # 如果用户已经登录，直接跳转到首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # 1. 从表单获取数据
        username = request.form['username']
        password = request.form['password']

        # 2. 在数据库中查找用户
        from models import User
        user = User.query.filter_by(username=username).first()

        # 3. 验证用户是否存在且密码正确
        if user is None or not user.check_password(password):
            # 如果验证失败，显示错误信息
            flash('用户名或密码错误，请重试。')
            return redirect(url_for('login'))  # 重定向回登录页面，会显示上面的flash消息

        # 4. 验证成功！调用 login_user 函数记录用户登录状态
        login_user(user)
        flash(f'欢迎回来，{username}！')

        # 5. 登录成功后，尝试跳转到用户原本想访问的页面（如果存在），否则回首页
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('index'))

    # 如果是GET请求，直接显示登录表单页面
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    """处理用户注册"""
    # 如果用户已登录，跳转到首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # 1. 从表单获取数据
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        # 2. 简单验证：两次密码是否一致
        if password != password2:
            flash('两次输入的密码不一致，请重新输入。')
            return redirect(url_for('register'))

        # 3. 检查用户名和邮箱是否已被占用
        from models import User
        if User.query.filter_by(username=username).first():
            flash('该用户名已被使用，请换一个。')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('该邮箱已被注册，请换一个。')
            return redirect(url_for('register'))

        # 4. 创建新用户
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # 使用安全的哈希方法存储密码
        db.session.add(new_user)
        db.session.commit()

        # 5. 注册成功后自动登录，并跳转到首页
        login_user(new_user)
        flash(f'注册成功！欢迎你，{username}。')
        return redirect(url_for('index'))

    # 如果是GET请求，显示注册表单
    return render_template('register.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已成功退出登录。')
    return redirect(url_for('index'))
# ！！！重要：确保在文件最底部！！！
if __name__ == '__main__':
    app.run(debug=True)