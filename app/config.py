from app.models import Students, Teachers, Class, Course,Grade,Score,Course_list_day,Course_list_id,Score_id
from app import db

def test():
    student1 = Students(name="小明", idnum="58822420007046280", stnum="123456789", phnum="15900000001",
                        email="758588888@qq.com")
    class1 = Class(name="1班", grade="2014级", place="3楼2教室" )
    teacher1 = Teachers(name="李杰", idnum="1255544488888", phnum="1584222222", email="2115656@qq.com")
    grade1 = Grade(grade_name="2014级")
    Course_list_id1= Course_list_id(course_list_name="2014级1班课程表")
    Course_list_day1 = Course_list_day(am1="1",am2="2",am3="3",am4="2")
    db.session.add(student1)
    class1.relate_student.append(student1)
    teacher1.relate_class.append(class1)
    teacher1.relate_student.append(student1)
    Course_list_id.relate_grade_course_list_id(grade1)
    Course_list_id.relate_course_list_id_class(student1)

    db.session.commit()

test()
