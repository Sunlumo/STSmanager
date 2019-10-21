from flask import Blueprint  # 前台home注册蓝图

home = Blueprint("home", __name__)

import app.home.views
