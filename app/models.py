from datetime import datetime
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from . import login_manager

# login_manager = LoginManager()
# # 如果没有登录则重定向到该蓝图的视图函数
# login_manager.login_view = "user.login"
# # 对登录用户进行监视,最高等级
# login_manager.session_protection = "strong"

# 定义用户数据模型
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 用户ID
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(255))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11))  # 电话号码
    info = db.Column(db.Text)  # 简介
    face = db.Column(db.String(255))  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志符
    userlog = db.relationship('Userlog', backref='user')  # 关联userlog表外键

    # def __init__(self, name, pwd):
    #     self.name = name
    #     self.pwd = pwd

    def __repr__(self):
        return '<User %r>' % self.name

    # 明文密码（只读）
    @property
    def password(self):
        raise AttributeError('文明密码不可读')

    # 写入密码，同时计算hash值，保存到模型中
    @password.setter
    def password(self, value):
        self.pwd = generate_password_hash(value)

    # 检查密码是否正确
    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)

    @login_manager.user_loader
    def load_user(user):
        return User.query.get(int(user))


# 定义用户登录日志数据模型
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 日志ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户ID，关联user表外键
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime(255), index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return '<Userlog %r>' % self.id


class Students(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    idnum = db.Column(db.String(100), unique=True)
    stnum = db.Column(db.String(100), unique=True)
    phnum = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(100), unique=True)
    grade = db.Column(db.String(100))
    class_id = db.Column(db.String(100))
    teacher_id = db.Column(db.String(100))
    course_id = db.Column(db.String(100))
    score_id = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Students %r>' % self.id


class Score_id(db.Model):
    __tablename__ = "score_id"
    id = db.Column(db.Integer, primary_key=True)
    stnum = db.Column(db.String(100), unique=True)
    score0_id = db.Column(db.String(100))
    score1_id = db.Column(db.String(100))
    score2_id = db.Column(db.String(100))
    score3_id = db.Column(db.String(100))
    score4_id = db.Column(db.String(100))
    score5_id = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    # relate_student_score = db.relationship('Students', backref='relate_score_id_students', lazy='dynamic')

    def __repr__(self):
        return '<Score_id %r>' % self.id


class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)
    stnum = db.Column(db.String(100), unique=True)
    score_num = db.Column(db.String(100))
    Math = db.Column(db.String(100))
    English = db.Column(db.String(100))
    Chinese = db.Column(db.String(100))
    Physics = db.Column(db.String(100))
    Chemistry = db.Column(db.String(100))
    Biology = db.Column(db.String(100))
    History = db.Column(db.String(100))
    Geography = db.Column(db.String(100))
    Politics = db.Column(db.String(100))
    Art = db.Column(db.String(100))
    Sports = db.Column(db.String(100))
    Technology = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Score_id %r>' % self.id


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    teacher_id = db.Column(db.String(100))
    msg = db.Column(db.Text)
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Course %r>' % self.id


class Course_list_id(db.Model):
    __tablename__ = "course_list_id"
    id = db.Column(db.Integer, primary_key=True)
    course_list_name = db.Column(db.String(100))
    grade = db.Column(db.String(100))
    classes_id = db.Column(db.String(100))
    Monday = db.Column(db.String(100))
    Tuesday = db.Column(db.String(100))
    Wednesday = db.Column(db.String(100))
    Thursday = db.Column(db.String(100))
    Friday = db.Column(db.String(100))
    msg = db.Column(db.Text)
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    # relate_course_student = db.relationship('Students', backref='relate_student_course_list_id', lazy='dynamic')
    # relate_courses = db.relationship('Course', backref='relate_course_list_id_courses', lazy='dynamic')

    def __repr__(self):
        return '<Course_list_id %r>' % self.id


class Course_list_day(db.Model):
    __tablename__ = "course_list_day"
    id = db.Column(db.Integer, primary_key=True)
    course_list_id = db.Column(db.String(100))
    am1 = db.Column(db.String(100))
    am2 = db.Column(db.String(100))
    am3 = db.Column(db.String(100))
    am4 = db.Column(db.String(100))
    pm1 = db.Column(db.String(100))
    pm2 = db.Column(db.String(100))
    pm3 = db.Column(db.String(100))
    pm4 = db.Column(db.String(100))
    nt1 = db.Column(db.String(100))
    nt2 = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Course_list_day %r>' % self.id


class Grade(db.Model):
    __tablename__ = "grade"
    id = db.Column(db.Integer, primary_key=True)
    grade_name = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    # relate_student_grade = db.relationship('Students', backref='relate_grade_students', lazy='dynamic')
    # relate_course_list_id_grade = db.relationship('Course_list_id', backref='relate_grade_course_list_id', lazy='dynamic')
    # relate_class_grade = db.relationship('Class', backref='relate_grade_class', lazy='dynamic')

    def __repr__(self):
        return '<Course_list_day %r>' % self.id


class Class(db.Model):
    __tablename__ = "class"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    grade = db.Column(db.String(100))
    place = db.Column(db.String(100))
    teacher_id = db.Column(db.String(100))
    msg = db.Column(db.Text)
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    # relate_class_student = db.relationship('Students', backref='relate_student_class', lazy='dynamic')
    # relate_class_course_list_id = db.relationship('Course_list_id', backref='relate_course_list_id_class', lazy='dynamic')


    def __repr__(self):
        return '<Class %r>' % self.id


class Teachers(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    idnum = db.Column(db.String(18), unique=True)
    name = db.Column(db.String(100), unique=True)
    phnum = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(100), unique=True)
    class_id = db.Column(db.String(100))
    course_id = db.Column(db.String(100))
    is_change = db.Column(db.String(10))
    msg = db.Column(db.Text)
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    # relate_student = db.relationship('Students', backref="relate_students_teacher", lazy='dynamic')
    # relate_class = db.relationship('Class', backref='relate_classes_teacher', lazy='dynamic')
    # relate_course = db.relationship('Course', backref='relate_courses_teacher', lazy='dynamic')

    def __repr__(self):
        return '<Teachers %r>' % self.id


db.drop_all()
db.create_all()

user = User(name="admin",
                 pwd="pbkdf2:sha256:150000$TbuwhsI6$fc3a786a0c23820a4fa197567d04b5bd5f6b755cac494f1bf2c101574231ce2d",
                 email="758588590@qq.com",
                 phone="15813413659",
                 info="jhah",
                 face="11",
                 addtime="2019-07-11",
                 uuid="1")

db.session.add(user)
db.session.commit()
