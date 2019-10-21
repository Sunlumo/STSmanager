from . import home
import time
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import *
from app.models import User, Userlog, Students, Teachers, Class, Grade, Score, Score_id, Course_list_id, \
    Course_list_day, Course
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_required, login_user
from datetime import timedelta
from app import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy import and_, or_


# from operator import or_, and_


# 登录首页
@home.route("/index")
@login_required
def index():
    # num = ["hello", "world", "I", "am", "H"]
    # user_id = session.get("user_id")
    user = User.query.get(session.get("user_id"))

    # form = Index()
    # print(form.data)
    # if form.submit_photo == True:
    #     return render_template("/home/photo.html")
    #     # return redirect(url_for("home.upphoto") or request.args.get("next"))

    return render_template("/home/index.html", user_name=user.name)


# 上传照片
@home.route("/photo", methods=["GET", "POST"])
@login_required
def upphoto():
    form = UpFile()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)  # 提取文件名
        form.photo.save('/uploads' + filename)
        print(filename)
        return render_template("home/index.html")

    return render_template("/home/photo.html", form=form)


# 用户登录
@home.route("/", methods=["GET", "POST"])
def login():  # 登录密码验证
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        user_count = User.query.filter_by(name=data["accent"]).count()
        user = User.query.filter_by(name=data["accent"]).first()
        print(user)
        # if user is not None and user.check_password(form.pwd):
        # login_user(user, remember=True)
        # return redirect(url_for("home.index") or request.args.get("next"))  # 跳转到/test路由
        #  else:
        #      flash("账号密码错误！")
        if user_count == 0:
            flash("账号不存在！")
            return redirect(url_for("home.login"))

        elif user_count == 1:
            if not user.check_pwd(data["pwd"]):
                flash("密码错误！")
                return redirect(url_for("home.login"))
            else:
                login_user(user, remember=form.remember_me.data)
                session.permanent = True  # 设置session永久有效
                app.permanent_session_lifetime = timedelta(minutes=30)  # 设置session 10分钟有效
                session["user"] = data["accent"]
                return redirect(url_for("home.index") or request.args.get("next"))  # 跳转到/test路由

        else:
            flash("请联系系统管理员！")
            return render_template("home/index.html")

    return render_template("home/login.html", form=form)


# 用户注册
@home.route("/registration/", methods=["POST", "GET"])
# @login_required
def registration():
    registration_form = RegistrationForm()  # 实例化表单类对象
    # request: 请求对象，获取请求方式，数据
    # 1、判断请求方式
    if request.method == 'POST':
        # 2、获取请求参数
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # password2 = request.form.get("password2")
        print(name, email, password)
        # 3、验证参数 需加入CSRF token验证
        if registration_form.validate_on_submit():
            if User.query.filter_by(name=name).first():
                flash("该用户名已被使用！")
                return redirect(url_for("home.registration") or request.args.get("next"))
            else:
                if User.query.filter_by(email=email).first():
                    flash("该邮箱已被使用！")
                    return redirect(url_for("home.registration") or request.args.get("next"))
                else:
                    try:
                        user_add = User(name=name, pwd=generate_password_hash(password), email=email)
                        db.session.add(user_add)
                        db.session.commit()
                        flash("注册成功，请登录！")
                        time.sleep(3)
                        return redirect(url_for("home.login"))
                    except Exception as e:
                        # 加入数据库commit提交失败，必须回滚！！！
                        db.session.rollback()
                        raise e
        else:
            flash("输入有误，请检查！")
    return render_template("home/register.html", form=registration_form)


# 找回密码
@home.route("/find_pwd/")
# @login_required
def find_pwd():
    # return redirect(url_for("home.find_pwd"))
    return render_template("home/find_pwd.html")


# 学员列表
@home.route("/student_g/<int:page>", methods=["POST", "GET"])
@login_required
def student_g(page):
    user = User.query.get(session.get("user_id"))
    student_query_form = Student_query()
    print(request.method)
    if request.method == "GET":
        pagination = Students.query.order_by(Students.add_time.desc()).paginate(page, per_page=10, error_out=False)
        st_list = pagination.items
    elif request.method == 'POST':
        name = request.form.get("name_idnum")
        idnum = request.form.get("name_idnum")
        stnum = request.form.get("stnum")
        email = request.form.get("email")
        phnum = request.form.get("phnum")
        addtime_s = request.form.get("addtime_s")
        if addtime_s == "":
            min_student = Students.query.order_by(Students.add_time).first()
            addtime_s = min_student.add_time
        addtime_e = request.form.get("addtime_e")
        if addtime_e == "":
            max_student = Students.query.order_by(Students.add_time.desc()).first()
            addtime_e = max_student.add_time
        print(name, idnum, stnum, email, phnum, addtime_e, addtime_s)
        try:
            pagination = Students.query.filter(
                and_(
                    Students.add_time >= addtime_s,
                    Students.add_time <= addtime_e,
                    Students.email.like("%{}%".format(email)),
                    Students.stnum.like("%{}%".format(stnum)),
                    or_(Students.idnum.like("%{}%".format(idnum)),
                        Students.name.like("%{}%".format(name))),
                    Students.phnum.like("%{}%".format(phnum))
                )
            ).order_by(Students.add_time.desc()).paginate(page, per_page=10, error_out=False)
            st_list = pagination.items
        except Exception as e:
            flash("查询失败，请稍后再试！")
            raise e
    return render_template("/home/student_g.html",
                           user_name=user.name,
                           st_list=st_list,
                           pagination=pagination,
                           form=student_query_form)


# 添加学生
@home.route("/student/add/", methods=["POST", "GET"])
@login_required
def student_add():
    user = User.query.get(session.get("user_id"))
    studentadd_form = Student_add()
    name = request.form.get("name")
    idnum = request.form.get("idnum")
    stnum = request.form.get("stnum")
    email = request.form.get("email")
    phnum = request.form.get("phnum")
    grade = request.form.get("grade")
    class_id = request.form.get("classes")
    teacher_id = request.form.get("teacher")
    print(class_id, teacher_id)
    if request.method == 'POST':
        if studentadd_form.validate_on_submit():
            if Students.query.filter_by(idnum=idnum).count():
                flash("该身份证号码已存在！", "idnum")
            if Students.query.filter_by(stnum=stnum).count():
                flash("该学号已存在！", "stnum")
            if Students.query.filter_by(phnum=phnum).count():
                flash("该电话号码已存在！", "phnum")
            if Students.query.filter_by(email=email).count():
                flash("该邮箱已存在！", "email")
            else:
                try:
                    student_add = Students(name=name,
                                           idnum=idnum,
                                           stnum=stnum,
                                           email=email,
                                           phnum=phnum,
                                           grade=grade,
                                           class_id=class_id.split(':')[0],
                                           teacher_id=teacher_id.split(':')[0]
                                           )
                    db.session.add(student_add)
                    db.session.commit()
                    flash("添加成功！", "other")
                    return redirect(url_for("home.student_add"))
                except Exception as e:
                    # 加入数据库commit提交失败，必须回滚！！！
                    db.session.rollback()
                    flash("添加失败，请稍后再试！", "other")
                    pass

    return render_template("/home/student_add.html", user_name=user.name, studentadd_form=studentadd_form)


# 编辑学生
@home.route("/student/edit/<int:id>", methods=["POST", "GET"])
@login_required
def student_edit(id):
    user = User.query.get(session.get("user_id"))
    student = Students.query.filter_by(id=id).first()
    student_edit_form = Student_add()
    name = request.form.get("name")
    idnum = request.form.get("idnum")
    stnum = request.form.get("stnum")
    email = request.form.get("email")
    phnum = request.form.get("phnum")
    if request.method == 'POST':
        if student_edit_form.validate_on_submit():
            try:
                student.name = name
                print(Students.query.filter(and_(Students.idnum == idnum, Students.id != id)).count())
                print(Students.id, id)
                if Students.query.filter(and_(Students.idnum == idnum, Students.id != id)).count() == 0:
                    student.idnum = idnum
                else:
                    if Students.query.filter(and_(Students.id != id, Students.idnum == idnum)).count() > 0:
                        flash("该身份证号码已存在！", "idnum")
                        return redirect(url_for("home.student_edit", id=student.id))
                if Students.query.filter(and_(Students.stnum == stnum, Students.id != id)).count() == 0:
                    student.idnum = idnum
                else:
                    if Students.query.filter(and_(Students.id != id, Students.stnum == stnum)).count() > 0:
                        flash("该学号已存在！", "stnum")
                        return redirect(url_for("home.student_edit", id=student.id))
                if Students.query.filter(and_(Students.phnum == phnum, Students.id != id)).count() == 0:
                    student.idnum = idnum
                else:
                    if Students.query.filter(and_(Students.id != id, Students.phnum == phnum)).count() > 0:
                        flash("该电话号码已存在！", "phnum")
                        return redirect(url_for("home.student_edit", id=student.id))
                if Students.query.filter(and_(Students.email == email, Students.id != id)).count() == 0:
                    student.idnum = idnum
                else:
                    if Students.query.filter(and_(Students.id != id, Students.email == email)).count() > 0:
                        flash("该邮箱已存在！", "email")
                        return redirect(url_for("home.student_edit", id=student.id))
                db.session.commit()
                flash("修改成功！", "other")
                return redirect(url_for("home.student_edit", id=student.id))
            except Exception as e:
                # 加入数据库commit提交失败，必须回滚！！！
                flash("修改失败，请稍后重试！")
                db.session.rollback()
                raise e

    return render_template("/home/student_edit.html",
                           user_name=user.name,
                           student_edit_form=student_edit_form,
                           student=student)


# 删除学生
@home.route("/student/del/<int:id>", methods=["POST", "GET"])
@login_required
def student_del(id):
    user = User.query.get(session.get("user_id"))
    st_list = Students.query.order_by(Students.add_time.desc()).all()
    try:
        student = Students.query.filter_by(id=id).first()
        db.session.delete(student)
        db.session.commit()
        flash("删除成功！")
        return redirect(url_for("home.student_g", page=1))
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        flash("删除失败，请稍后重试！")
        db.session.rollback()
        raise e
    return render_template("/home/student_g.html", user_name=user.name, st_list=st_list)


"""
@home.route("/student/query/", methods=["POST", "GET"])
@login_required
def student_query():
    user = User.query.get(session.get("user_id"))
    student_query_form = Student_query()
    if request.method == 'POST':
        name = request.form.get("name_idnum")
        idnum = request.form.get("name_idnum")
        stnum = request.form.get("stnum")
        email = request.form.get("email")
        phnum = request.form.get("phnum")
        addtime_s = request.form.get("addtime_s")
        addtime_e = request.form.get("addtime_e")
        if student_query_form.validate_on_submit():
            # try:
            st_list = session.query(Students).filter(
                and_(
                    Students.add_time >= addtime_s,
                    Students.add_time <= addtime_e,
                    Students.email == email,
                    Students.idnum.like("%idnum%"),
                    Students.name.like("%name%"),
                    Students.phnum.like("%phnum%")
                )
            ).all()
            # return redirect(url_for("home.student_g"))
            # except Exception as e:
            flash("查询失败，请稍后重试！")
            # raise e

    return render_template("/home/student_g.html",
                           user_name=user.name,
                           st_list=st_list,
                           form=student_query_form)
"""


# 教师管理
@home.route("/teacher_g/<int:page>", methods=["POST", "GET"])
@login_required
def teacher_g(page=None):
    user = User.query.get(session.get("user_id"))
    teacher_query_form = Teacher_query()
    print(request.method)
    if request.method == "GET":
        pagination = Teachers.query.order_by(Teachers.add_time.desc()).paginate(page, per_page=10, error_out=False)
        th_list = pagination.items
    elif request.method == 'POST':
        name = request.form.get("name_idnum")
        idnum = request.form.get("name_idnum")
        email = request.form.get("email")
        phnum = request.form.get("phnum")
        addtime_s = request.form.get("addtime_s")
        if addtime_s == "":
            min_teacher = Teachers.query.order_by(Teachers.add_time).first()
            addtime_s = min_teacher.add_time
        addtime_e = request.form.get("addtime_e")
        if addtime_e == "":
            max_teacher = Teachers.query.order_by(Teachers.add_time.desc()).first()
            addtime_e = max_teacher.add_time
        print(name, idnum, email, phnum, addtime_e, addtime_s)
        try:
            pagination = Teachers.query.filter(
                and_(
                    Teachers.add_time >= addtime_s,
                    Teachers.add_time <= addtime_e,
                    Teachers.email.like("%{}%".format(email)),
                    or_(Teachers.idnum.like("%{}%".format(idnum)),
                        Teachers.name.like("%{}%".format(name))),
                    Teachers.phnum.like("%{}%".format(phnum))
                )
            ).order_by(Teachers.add_time.desc()).paginate(page, per_page=1, error_out=False)
            th_list = pagination.items
        except Exception as e:
            flash("查询失败，请稍后再试！")
            raise e
    return render_template("/home/teacher_g.html",
                           user_name=user.name,
                           th_list=th_list,
                           pagination=pagination,
                           form=teacher_query_form)


# 添加教师
@home.route("/teacher_add/", methods=["POST", "GET"])
@login_required
def teacher_add():
    user = User.query.get(session.get("user_id"))
    teacheradd_form = Teacher_add()
    if request.method == 'POST':
        name = request.form.get("name")
        idnum = request.form.get("idnum")
        email = request.form.get("email")
        phnum = request.form.get("phnum")
        course_id = request.form.get("course_id")
        msg = request.form.get("msg")
        if teacheradd_form.validate_on_submit():
            if Teachers.query.filter_by(idnum=idnum).count():
                flash("该身份证号码已存在！", "idnum")
            if Teachers.query.filter_by(phnum=phnum).count():
                flash("该电话号码已存在！", "phnum")
            if Teachers.query.filter_by(email=email).count():
                flash("该邮箱已存在！", "email")
            else:
                try:
                    teacher_add = Teachers(name=name,
                                           idnum=idnum,
                                           email=email,
                                           phnum=phnum,
                                           course_id=course_id,
                                           msg=msg
                                           )
                    db.session.add(teacher_add)
                    db.session.commit()
                    flash("添加成功！", "other")
                    return redirect(url_for("home.teacher_add"))
                except Exception as e:
                    # 加入数据库commit提交失败，必须回滚！！！
                    db.session.rollback()
                    flash("添加失败，请稍后再试！", "other")
                    pass

    return render_template("/home/teacher_add.html", user_name=user.name, teacheradd_form=teacheradd_form)


# 编辑教师
@home.route("/teacher_edit/<int:id>", methods=["POST", "GET"])
@login_required
def teacher_edit(id):
    user = User.query.get(session.get("user_id"))
    teacher_edit_form = Teacher_add()
    teacher = Teachers.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form.get("name")
        idnum = request.form.get("idnum")
        email = request.form.get("email")
        phnum = request.form.get("phnum")
        course_id = request.form.get("course_id")
        msg = request.form.get("msg")
        print(name, idnum, email, phnum)
        if teacher_edit_form.validate_on_submit():
            try:
                teacher.name = name
                teacher.course_id = course_id
                teacher.msg = msg
                print(Teachers.query.filter(and_(Teachers.idnum == idnum, Teachers.id != id)).count())
                print(Teachers.id, id)
                if Teachers.query.filter(and_(Teachers.idnum == idnum, Teachers.id != id)).count() == 0:
                    teacher.idnum = idnum
                else:
                    if Teachers.query.filter(and_(Teachers.id != id, Teachers.idnum == idnum)).count() > 0:
                        flash("该身份证号码已存在！", "idnum")
                        return redirect(url_for("home.teacher_edit", id=teacher.id))
                if Teachers.query.filter(and_(Teachers.phnum == phnum, Teachers.id != id)).count() == 0:
                    teacher.phnum = phnum
                else:
                    if Teachers.query.filter(and_(Teachers.id != id, Teachers.phnum == phnum)).count() > 0:
                        flash("该电话号码已存在！", "phnum")
                        return redirect(url_for("home.teacher_edit", id=teacher.id))
                if Teachers.query.filter(and_(Teachers.email == email, Teachers.id != id)).count() == 0:
                    teacher.email = email
                else:
                    if Teachers.query.filter(and_(Teachers.id != id, Teachers.email == email)).count() > 0:
                        flash("该邮箱已存在！", "email")
                        return redirect(url_for("home.teacher_edit", id=teacher.id))
                db.session.commit()
                flash("修改成功！", "other")
                return redirect(url_for("home.teacher_edit", id=teacher.id))
            except Exception as e:
                # 加入数据库commit提交失败，必须回滚！！！
                flash("修改失败，请稍后重试！")
                db.session.rollback()
                raise e

    return render_template("/home/teacher_edit.html",
                           user_name=user.name,
                           teacher_edit_form=teacher_edit_form,
                           teacher=teacher)


# 删除教师
@home.route("/teacher_del/<int:id>", methods=["POST", "GET"])
@login_required
def teacher_del(id):
    user = User.query.get(session.get("user_id"))
    th_list = Teachers.query.order_by(Teachers.add_time.desc()).all()
    try:
        teacher = Teachers.query.filter_by(id=id).first()
        db.session.delete(teacher)
        db.session.commit()
        flash("删除成功！")
        return redirect(url_for("home.teacher_g", page=1))
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        flash("删除失败，请稍后重试！")
        db.session.rollback()
        raise e
    return render_template("/home/teacher_g.html", user_name=user.name, th_list=th_list)


# 班级管理
@home.route("/class_g/<int:page>", methods=["POST", "GET"])
@login_required
def class_g(page=None):
    user = User.query.get(session.get("user_id"))
    class_query_form = Class_query()
    print(request.method)
    if request.method == "GET":
        pagination = Class.query.order_by(Class.add_time.desc()).paginate(page, per_page=10, error_out=False)
        class_list = pagination.items
    elif request.method == 'POST':
        name = request.form.get("name")
        place = request.form.get("place")
        teacher_id = request.form.get("teacher_id")
        grade = request.form.get("grade")
        addtime_s = request.form.get("addtime_s")
        addtime_e = request.form.get("addtime_e")
        print(name, place, grade, teacher_id, addtime_e, addtime_s)
        if Class.query.count() == 0:
            flash("无数据！")
            return redirect(url_for("home.class_g", page=1))
        else:
            if addtime_s == "":
                min_Class = Class.query.order_by(Class.add_time).first()
                addtime_s = min_Class.add_time
            if addtime_e == "":
                max_Class = Class.query.order_by(Class.add_time.desc()).first()
                addtime_e = max_Class.add_time
            print(name, place, grade, teacher_id, addtime_e, addtime_s)
            try:
                if grade == "0" and teacher_id == "0":
                    pagination = Class.query.filter(
                        and_(
                            Class.add_time >= addtime_s,
                            Class.add_time <= addtime_e,
                            Class.place.like("%{}%".format(place)),
                            Class.name.like("%{}%".format(name)),
                        )
                    ).order_by(Class.add_time.desc()).paginate(page, per_page=10, error_out=False)
                elif grade != "0" and teacher_id != "0":
                    pagination = Class.query.filter(
                        and_(
                            Class.add_time >= addtime_s,
                            Class.add_time <= addtime_e,
                            Class.place.like("%{}%".format(place)),
                            Class.name.like("%{}%".format(name)),
                            Class.grade.like("%{}%".format(grade)),
                            Class.teacher_id.like("%{}%".format(teacher_id))
                        )
                    ).order_by(Class.add_time.desc()).paginate(page, per_page=10, error_out=False)
                else:
                    pagination = Class.query.filter(
                        and_(
                            Class.add_time >= addtime_s,
                            Class.add_time <= addtime_e,
                            Class.place.like("%{}%".format(place)),
                            or_(
                                Class.name.like("%{}%".format(name)),
                                Class.grade.like("%{}%".format(grade))
                            ),
                            Class.teacher_id.like("%{}%".format(teacher_id))
                        )
                    ).order_by(Class.add_time.desc()).paginate(page, per_page=10, error_out=False)
                class_list = pagination.items
            except Exception as e:
                flash("查询失败，请稍后再试！")
                raise e
    return render_template("/home/class.html",
                           user_name=user.name,
                           class_list=class_list,
                           pagination=pagination,
                           form=class_query_form)


# 添加班级
@home.route("/class_add/", methods=["POST", "GET"])
@login_required
def class_add():
    user = User.query.get(session.get("user_id"))
    class_add_form = Class_add()
    if request.method == 'POST':
        name = request.form.get("name")
        place = request.form.get("place")
        teacher_id = request.form.get("teacher_id")
        grade = request.form.get("grade")
        msg = request.form.get("msg")
        if class_add_form.validate_on_submit():
            if Class.query.filter_by(place=place).count():
                flash("该教室已被使用！", "place")
            if Class.query.filter_by(name=name, grade=grade).count():
                flash("该班级存在！", "name")
            else:
                try:
                    class_add = Class(name=name, place=place, grade=grade, teacher_id=teacher_id, msg=msg)
                    db.session.add(class_add)
                    db.session.commit()
                    flash("添加成功！", "other")
                    return redirect(url_for("home.class_add"))
                except Exception as e:
                    # 加入数据库commit提交失败，必须回滚！！！
                    db.session.rollback()
                    flash("添加失败，请稍后再试！", "other")
                    pass

    return render_template("/home/class_add.html", user_name=user.name, class_add_form=class_add_form)


# 编辑班级
@home.route("/class_edit/<int:id>", methods=["POST", "GET"])
@login_required
def class_edit(id):
    user = User.query.get(session.get("user_id"))
    class_edit_form = Class_add()
    classes = Class.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form.get("name")
        place = request.form.get("place")
        teacher_id = request.form.get("teacher_id")
        grade = request.form.get("grade")
        msg = request.form.get("msg")
        if class_edit_form.validate_on_submit():
            try:
                classes.teacher_id = teacher_id
                classes.msg = msg
                if Class.query.filter(and_(Class.name == name, Class.grade == grade, Teachers.id != id)).count() == 0:
                    classes.name = name
                    classes.grade = grade
                elif Class.query.filter(and_(Class.id != id, Class.place == place, Class.grade == grade, )).count() > 0:
                    flash("该班级已存在！", "place")
                    return redirect(url_for("home.class_edit", id=classes.id))
                else:
                    pass
                db.session.commit()
                flash("修改成功！", "other")
                return redirect(url_for("home.class_edit", id=classes.id))
            except Exception as e:
                # 加入数据库commit提交失败，必须回滚！！！
                flash("修改失败，请稍后重试！")
                db.session.rollback()
                raise e

    return render_template("/home/class_edit.html",
                           user_name=user.name,
                           class_edit_form=class_edit_form,
                           classes=classes)


# 删除班级
@home.route("/class_del/<int:id>", methods=["POST", "GET"])
@login_required
def class_del(id):
    user = User.query.get(session.get("user_id"))
    class_list = Class.query.order_by(Class.add_time.desc()).all()
    try:
        classes = Class.query.filter_by(id=id).first()
        db.session.delete(classes)
        db.session.commit()
        flash("删除成功！")
        return redirect(url_for("home.class_g", page=1))
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        flash("删除失败，请稍后重试！")
        db.session.rollback()
        raise e
    return render_template("/home/class.html", user_name=user.name, class_list=class_list)


# 年级管理
@home.route("/grade/<int:page>", methods=["POST", "GET"])
@login_required
def grade(page=None):
    user = User.query.get(session.get("user_id"))
    grade_query_form = Grade_query()
    print(request.method)
    if request.method == "GET":
        pagination = Grade.query.order_by(Grade.add_time.desc()).paginate(page, per_page=10, error_out=False)
        grade_list = pagination.items
    elif request.method == 'POST':
        name = request.form.get("name")
        addtime_s = request.form.get("addtime_s")
        addtime_e = request.form.get("addtime_e")
        print(name, addtime_e, addtime_s)
        if Grade.query.count() == 0:
            flash("无数据！")
            return redirect(url_for("home.grade", page=1))
        else:
            if addtime_s == "":
                min_Grade = Grade.query.order_by(Grade.add_time).first()
                addtime_s = min_Grade.add_time
            if addtime_e == "":
                max_Grade = Grade.query.order_by(Grade.add_time.desc()).first()
                addtime_e = max_Grade.add_time
            print(name, addtime_e, addtime_s)
            try:
                pagination = Grade.query.filter(
                    and_(
                        Grade.add_time >= addtime_s,
                        Grade.add_time <= addtime_e,
                        Grade.name.like("%{}%".format(name)),
                    )
                ).order_by(Grade.add_time.desc()).paginate(page, per_page=10, error_out=False)
                grade_list = pagination.items
            except Exception as e:
                flash("查询失败，请稍后再试！")
                raise e
    return render_template("/home/grade.html", user_name=user.name, grade_list=grade_list, pagination=pagination,
                           form=grade_query_form)


# 添加年级
@home.route("/grade_add/", methods=["POST", "GET"])
@login_required
def grade_add():
    user = User.query.get(session.get("user_id"))
    grade_add_form = Grade_add()
    if request.method == 'POST':
        grade_name = request.form.get("name")
        if grade_add_form.validate_on_submit():
            if Grade.query.filter_by(name=grade_name).count():
                flash("该年级已存在！", "name")
            else:
                try:
                    grade_add = Grade(name=grade_name)
                    db.session.add(grade_add)
                    db.session.commit()
                    flash("添加成功！", "other")
                    return redirect(url_for("home.grade_add"))
                except Exception as e:
                    # 加入数据库commit提交失败，必须回滚！！！
                    db.session.rollback()
                    flash("添加失败，请稍后再试！", "other")
                    pass

    return render_template("/home/grade_add.html", user_name=user.name, grade_add_form=grade_add_form)


# 编辑年级
@home.route("/grade_edit/<int:id>", methods=["POST", "GET"])
@login_required
def grade_edit(id):
    user = User.query.get(session.get("user_id"))
    grade_edit_form = Grade_add()
    grade = Grade.query.filter_by(id=id).first()
    if request.method == 'POST':
        grade_name = request.form.get("name")
        if grade_edit_form.validate_on_submit():
            try:
                if Grade.query.filter(and_(Grade.grade_name == grade_name, Grade.id != id)).count() == 0:
                    grade.name = grade_name
                elif Grade.query.filter(and_(Grade.grade_name == grade_name, Grade.id != id)).count() > 0:
                    flash("该班级已存在！", "place")
                    return redirect(url_for("home.class_edit", id=grade.id))
                else:
                    pass
                db.session.commit()
                flash("修改成功！", "other")
                return redirect(url_for("home.class_edit", id=grade.id))
            except Exception as e:
                # 加入数据库commit提交失败，必须回滚！！！
                flash("修改失败，请稍后重试！")
                db.session.rollback()
                raise e

    return render_template("/home/grade_edit.html",
                           user_name=user.name,
                           grade_edit_form=grade_edit_form,
                           grade=grade)


# 删除年级
@home.route("/grade_del/<int:id>", methods=["POST", "GET"])
@login_required
def grade_del(id):
    user = User.query.get(session.get("user_id"))
    grade_list = Class.query.order_by(Grade.add_time.desc()).all()
    try:
        grade = Class.query.filter_by(id=id).first()
        db.session.delete(grade)
        db.session.commit()
        flash("删除成功！")
        return redirect(url_for("home.grade", page=1))
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        flash("删除失败，请稍后重试！")
        db.session.rollback()
        raise e
    return render_template("/home/grade.html", user_name=user.name, grade_list=grade_list)


# 添加课程
@home.route("/course_add/", methods=["POST", "GET"])
@login_required
def course_add():
    user = User.query.get(session.get("user_id"))
    course_add_form = Course_add()
    if request.method == 'POST':
        course_name = request.form.get("name")
        if course_add_form.validate_on_submit():
            if Course.query.filter_by(name=course_name).count():
                flash("该课程已存在！", "name")
            else:
                try:
                    course_add = Course(name=course_name)
                    db.session.add(course_add)
                    db.session.commit()
                    flash("添加成功！", "other")
                    return redirect(url_for("home.course_add"))
                except Exception as e:
                    # 加入数据库commit提交失败，必须回滚！！！
                    db.session.rollback()
                    flash("添加失败，请稍后再试！", "other")
                    pass

    return render_template("/home/course_add.html", user_name=user.name, course_add_form=course_add_form)


# 编辑课程
@home.route("/course_edit/<int:id>", methods=["POST", "GET"])
@login_required
def course_edit(id):
    user = User.query.get(session.get("user_id"))
    course_edit_form = Course_add()
    course = Course.query.filter_by(id=id).first()
    if request.method == 'POST':
        course_name = request.form.get("name")
        teacher_id = request.form.get("teacher_id")
        if course_edit_form.validate_on_submit():
            try:
                course.teacher_id = teacher_id
                if Course.query.filter(and_(Course.course_name == course_name, Course.id != id)).count() == 0:
                    course.name = course_name
                elif Course.query.filter(and_(Course.course_name == course_name, Course.id != id)).count() > 0:
                    flash("该课程已存在！", "place")
                    return redirect(url_for("home.course_edit", id=course.id))
                else:
                    pass
                db.session.commit()
                flash("修改成功！", "other")
                return redirect(url_for("home.course_edit", id=course.id))
            except Exception as e:
                # 加入数据库commit提交失败，必须回滚！！！
                flash("修改失败，请稍后重试！")
                db.session.rollback()
                raise e

    return render_template("/home/course_edit.html",
                           user_name=user.name,
                           course_edit_form=course_edit_form,
                           course=course)


# 删除课程
@home.route("/course_del/<int:id>", methods=["POST", "GET"])
@login_required
def course_del(id):
    user = User.query.get(session.get("user_id"))
    course_list = Course.query.order_by(Course.add_time.desc()).all()
    try:
        course = Course.query.filter_by(id=id).first()
        db.session.delete(course)
        db.session.commit()
        flash("删除成功！")
        return redirect(url_for("home.course", page=1))
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        flash("删除失败，请稍后重试！")
        db.session.rollback()
        raise e
    return render_template("/home/course.html", user_name=user.name, course_list=course_list)


# 退出
@home.route("/logout/")
@login_required
def loginout():
    # db.session.pop(login_user("a"))
    return redirect(url_for("home.login"))  # 跳转指向home.login视图
