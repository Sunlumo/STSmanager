from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_login import LoginManager

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@127.0.0.1:3306/test?charset=utf8"  # 配置连接到数据库
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'd7465828b7da4daf87a8d2166269946b'
app.debug = True
db = SQLAlchemy(app)

login_manager = LoginManager(app)  # 注册loginager
login_manager.login_view = 'home.login'  # 检查未登录跳转视图
login_manager.login_message = '你必须登陆后才能访问该页面'  # 自定义弹出消息
login_manager.login_message_category = "info"  # 自定义消息级别，一般设置为info/error
login_manager.session_protection = "strong"  # 定义用户监视级别

# db.drop_all()
# db.create_all()

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")  # 蓝图指定首页路由
