from flask_wtf import FlaskForm, form
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo, Regexp
from app.models import User, Students, Teachers, Class
from app.models import db


def teacher_query_factory():
    teacher_list = []
    for r in db.session.query(Teachers).all():
        teacher = str(r.id) + ":" + r.name
        teacher_list.append(teacher)
    return teacher_list


def class_query_factory():
    class_list = []
    for r in db.session.query(Class).all():
        classes = str(r.id) + ":" + r.name
        class_list.append(classes)
    return class_list


# def grade_query_factory(self):
#     return [r.name for r in Teachers.query.all()]

def get_pk(obj):
    return obj


class LoginForm(FlaskForm):
    """管理员登录表单验证"""
    accent = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "placeholder": "请输入账号",
            "required": "required"
        }
    )

    pwd = PasswordField(
        label="账号",
        validators=[
            DataRequired("请输入密码!")
        ],
        description="账号",
        render_kw={
            "placeholder": "请输入密码",
            "required": "required"
        }
    )

    submit = SubmitField(
        label='登录',
        render_kw={
        })

    remember_me = BooleanField(
        label="记住密码",
        description="记住密码",
        render_kw={"placeholder": "记住密码"}
    )

    def validata_accent(self, field):
        accent = field.data
        user = User.query.filter_by(name=accent).count()
        if user == 0:
            raise ValidationError("账号不存在！")


class UpFile(FlaskForm):
    photo = FileField("MY PHOTO")
    submit = SubmitField("点击提交")


class Index(FlaskForm):
    submit_photo = SubmitField(
        label="点击上传图片",
        render_kw={
        })


class RegistrationForm(FlaskForm):
    email = StringField(label='邮箱',
                        validators=[DataRequired(message="请填写邮箱"),
                                    Length(1, 64),
                                    Email(message="请填写正确的邮箱！")
                                    ])
    username = StringField(label='用户名',
                           validators=[DataRequired(),
                                       Length(1, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              '用户名必须是字母、数字！')
                                       ])
    password = PasswordField(label='密码',
                             validators=[DataRequired(),
                                         ])
    password2 = PasswordField(label='确认密码',
                              validators=[DataRequired(), EqualTo('password',
                                                                  message='两次密码必须一致')])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被使用！')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('该用户名已被使用！')


class Student_add(FlaskForm):
    name = StringField(label='姓名',
                       validators=[DataRequired(message="请填写姓名"),
                                   Length(1, 10)])

    idnum = StringField(label='身份证号码',
                        validators=[DataRequired(message="请填写身份证号码"),
                                    Length(1, 18)])

    stnum = StringField(label='学号',
                        validators=[DataRequired(message="请填写学号")])

    phnum = StringField(label='电话号码',
                        validators=[DataRequired(message="请填写身电话号码"),
                                    Length(1, 13)])

    email = StringField(label='邮箱',
                        validators=[DataRequired(message="请填写邮箱"),
                                    Length(1, 18), Email(message="请填写正确的邮箱！")])

    grade = SelectField(label='年级',
                        validators=[DataRequired(message="请选择年级")],
                        render_kw={'class': 'form-control', "id": "sel_grade"},
                        choices=[(0, '请选择年级'), (1, '2018级'), (2, '2019级'), (3, '2020级')],
                        coerce=int
                        )

    classes = QuerySelectField(label='班级',
                               validators=[DataRequired(message="请选择班级")],
                               render_kw={'class': 'form-control', "id": "sel_grade"},
                               query_factory=class_query_factory, get_pk=get_pk,
                               blank_text="请选择班级",
                               allow_blank=True
                               )

    teacher = QuerySelectField(label='班主任',
                               validators=[DataRequired(message="请选择班主任")],
                               render_kw={'class': 'form-control', "id": "sel_teacher_id"},
                               query_factory=teacher_query_factory, get_pk=get_pk,
                               blank_text='请选择班主任',
                               allow_blank=True)

    submit = SubmitField('提交')


class StudentsVerify:
    def validate_email(self, field):
        if Students.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已存在！')

    def validate_idnum(self, field):
        if Students.query.filter_by(idnum=field.data).first():
            raise ValidationError('该身份证号码已存在！')

    def validate_stnum(self, field):
        if Students.query.filter_by(stnum=field.data).first():
            raise ValidationError('该学号已存在！')

    def validate_phnum(self, field):
        if Students.query.filter_by(phnum=field.data).first():
            raise ValidationError('该电话号码已存在！')


class Student_query(FlaskForm):
    name_idnum = StringField(label='姓名',
                             validators=[Length(1, 18)],
                             render_kw={"placeholder": "请输入学员姓名或证件号码",
                                        "type": "text",
                                        "autocomplete": "off"
                                        })

    stnum = StringField(label='学号',
                        validators=[Length(1, 18)],
                        render_kw={"placeholder": "请输入学号",
                                   "type": "text",
                                   "autocomplete": "off"
                                   })

    phnum = StringField(label='电话号码',
                        validators=[Length(1, 13)],
                        render_kw={"placeholder": "请输入电话号码",
                                   "type": "text",
                                   "autocomplete": "off"
                                   })

    email = StringField(label='邮箱',
                        validators=[Email(message="请填写正确的邮箱！")],
                        render_kw={"placeholder": "请输入邮箱",
                                   "type": "text",
                                   "autocomplete": "off"})

    addtime_s = StringField(label='创建时间始',
                            render_kw={"placeholder": "请输入创建时间始",
                                       "type": "text",
                                       "autocomplete": "off"})

    addtime_e = StringField(label='创建时间止',
                            # validators=[],
                            render_kw={"placeholder": "请输入创建时间始止",
                                       "type": "text",
                                       "autocomplete": "off"})

    submit_query = SubmitField("查询",
                               render_kw={"class": "class_g_butten",
                                          "style": "left:190px"}
                               )


class Teacher_add(FlaskForm):
    name = StringField(label='姓名',
                       validators=[DataRequired(message="请填写姓名"),
                                   Length(1, 10)])

    idnum = StringField(label='身份证号码',
                        validators=[DataRequired(message="请填写身份证号码"),
                                    Length(1, 18)])

    # class_id = QuerySelectField(label='班级',
    #                             validators=[DataRequired(message="请选择班级")],
    #                             render_kw={'class': 'form-control', "id": "sel_grade"},
    #                             query_factory=class_query_factory, get_pk=get_pk,
    #                             blank_text="请选择班级",
    #                             allow_blank=True
    #                             )

    course_id = SelectField(label="课程",
                            validators=[DataRequired(message="请选择课程")],
                            render_kw={'class': 'form-control', "id": "sel_course_id"},
                            choices=[(0, '请选择'), (1, '语文'), (2, '数学'), (3, '英语')],
                            # defalut=3,
                            coerce=int)

    phnum = StringField(label='电话号码',
                        validators=[DataRequired(message="请填写身电话号码"),
                                    Length(1, 13)])

    email = StringField(label='邮箱',
                        validators=[DataRequired(message="请填写邮箱"),
                                    Length(1, 18), Email(message="请填写正确的邮箱！")])

    msg = StringField(label="备注",
                      validators=[Length(0, 100)]
                      )

    submit = SubmitField('提交')


class TeacherVerify:
    def validate_email(self, field):
        if Teachers.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已存在！')

    def validate_idnum(self, field):
        if Teachers.query.filter_by(idnum=field.data).first():
            raise ValidationError('该身份证号码已存在！')

    def validate_phnum(self, field):
        if Teachers.query.filter_by(phnum=field.data).first():
            raise ValidationError('该电话号码已存在！')


class Teacher_query(FlaskForm):
    name_idnum = StringField(label='姓名',
                             validators=[Length(1, 18)],
                             render_kw={"placeholder": "请输入学员姓名或证件号码",
                                        "type": "text",
                                        "autocomplete": "off"
                                        })

    phnum = StringField(label='电话号码',
                        validators=[Length(1, 13)],
                        render_kw={"placeholder": "请输入电话号码",
                                   "type": "text",
                                   "autocomplete": "off"
                                   })

    email = StringField(label='邮箱',
                        validators=[Length(1, 30)],
                        render_kw={"placeholder": "请输入邮箱",
                                   "type": "text",
                                   "autocomplete": "off"})

    addtime_s = StringField(label='创建时间始',
                            render_kw={"placeholder": "请输入创建时间始",
                                       "type": "text",
                                       "autocomplete": "off"})

    addtime_e = StringField(label='创建时间止',
                            # validators=[],
                            render_kw={"placeholder": "请输入创建时间始止",
                                       "type": "text",
                                       "autocomplete": "off"})

    submit_query = SubmitField("查询",
                               render_kw={"class": "class_g_butten",
                                          "style": "left:190px"}
                               )


class Class_add(FlaskForm):
    name = StringField(label='名称',
                       validators=[DataRequired(message="请填写名称"),
                                   Length(1, 10)])

    place = StringField(label='地点',
                        validators=[DataRequired(message="请填写地点"),
                                    Length(1, 10)])

    grade = SelectField(label='年级',
                        validators=[DataRequired(message="请选择年级")],
                        render_kw={'class': 'form-control', "id": "sel_grade"},
                        choices=[(0, '请选择年级'), (1, '2018级'), (2, '2019级'), (3, '2020级')],
                        coerce=int
                        )

    teacher_id = QuerySelectField(label='班主任',
                                  validators=[DataRequired(message="请选择班主任")],
                                  render_kw={'class': 'form-control', "id": "sel_teacher_id"},
                                  query_factory=teacher_query_factory, get_pk=get_pk,
                                  blank_text='请选择班主任',
                                  allow_blank=True)

    msg = StringField(label="备注",
                      validators=[Length(0, 100)]
                      )

    submit = SubmitField('提交')


class Class_query(FlaskForm):
    name = StringField(label='名称',
                       validators=[Length(1, 10)],
                       render_kw={"placeholder": "请输入名称",
                                  "type": "text",
                                  "autocomplete": "off"})

    place = StringField(label='地点',
                        validators=[Length(1, 10)],
                        render_kw={"placeholder": "请输入地点",
                                   "type": "text",
                                   "autocomplete": "off"})

    grade = SelectField(label='年级',
                        validators=[DataRequired(message="请选择年级")],
                        render_kw={'class': 'form-control', "id": "sel_grade"},
                        choices=[(0, '请选择年级'), (1, '2018级'), (2, '2019级'), (3, '2020级')],
                        coerce=int
                        )

    teacher_id = QuerySelectField(label='班主任',
                                  validators=[DataRequired(message="请选择班主任")],
                                  render_kw={'class': 'form-control', "id": "sel_teacher_id"},
                                  query_factory=teacher_query_factory, get_pk=get_pk,
                                  blank_text='请选择班主任',
                                  allow_blank=True)

    addtime_s = StringField(label='创建时间始',
                            render_kw={"placeholder": "请输入创建时间始",
                                       "type": "text",
                                       "autocomplete": "off"})

    addtime_e = StringField(label='创建时间止',
                            render_kw={"placeholder": "请输入创建时间始止",
                                       "type": "text",
                                       "autocomplete": "off"})

    submit = SubmitField('提交')


class Grade_add(FlaskForm):
    grade_name = StringField(label='名称',
                             validators=[DataRequired(message="请填写名称"),
                                         Length(1, 10)])

    submit = SubmitField('提交')


class Grade_query(FlaskForm):
    grade_name = StringField(label='名称',
                             render_kw={"placeholder": "请输入名称",
                                        "type": "text",
                                        "autocomplete": "off"})

    addtime_s = StringField(label='创建时间始',
                            render_kw={"placeholder": "请输入创建时间始",
                                       "type": "text",
                                       "autocomplete": "off"})

    addtime_e = StringField(label='创建时间止',
                            render_kw={"placeholder": "请输入创建时间始止",
                                       "type": "text",
                                       "autocomplete": "off"})

    submit = SubmitField('提交')


class Course_add(FlaskForm):
    course_name = StringField(label='名称',
                              validators=[DataRequired(message="请填写名称"),
                                          Length(1, 10)])

    teacher_id = QuerySelectField(label='班主任',
                                  validators=[DataRequired(message="请选择班主任")],
                                  render_kw={'class': 'form-control', "id": "sel_teacher_id"},
                                  query_factory=teacher_query_factory, get_pk=get_pk,
                                  blank_text='请选择班主任',
                                  allow_blank=True)

    msg = StringField(label="备注",
                      validators=[Length(0, 100)]
                      )

    submit = SubmitField('提交')


class Course_query(FlaskForm):
    course_name = StringField(label='名称',
                              render_kw={"placeholder": "请输入创建时间始",
                                         "type": "text",
                                         "autocomplete": "off"})

    teacher_id = QuerySelectField(label='班主任',
                                  render_kw={'class': 'form-control', "id": "sel_teacher_id"},
                                  query_factory=teacher_query_factory, get_pk=get_pk,
                                  blank_text='请选择班主任',
                                  allow_blank=True)

    addtime_s = StringField(label='创建时间始',
                            render_kw={"placeholder": "请输入创建时间始",
                                       "type": "text",
                                       "autocomplete": "off"})

    addtime_e = StringField(label='创建时间止',
                            render_kw={"placeholder": "请输入创建时间始止",
                                       "type": "text",
                                       "autocomplete": "off"})

    submit = SubmitField('提交')
