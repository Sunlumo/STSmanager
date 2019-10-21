from flask import Blueprint  # 后台admin注册蓝图

admin = Blueprint("admin", __name__)

import app.admin.views