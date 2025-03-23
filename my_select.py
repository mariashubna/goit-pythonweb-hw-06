from models import Student, Teacher, Group, Subject, Grade, association_table
from connect import engine, session
from sqlalchemy import func
import random


def select_1():
    students = (
        session.query(
            Student.id,
            Student.first_name,
            Student.last_name,
            func.round(func.avg(Grade.grade), 1).label("avg_grade"),
        )
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )

    print("The best 5 students:")
    for row in students:
        print(row)


def select_2(subject_name):

    best_student = (
        session.query(
            Student.first_name,
            Student.last_name,
            func.round(func.avg(Grade.grade), 1).label("avg_grade"),
        )
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
        .first()
    )

    if best_student:
        print(
            f"Best student in {subject_name}: {best_student.first_name} {best_student.last_name}, AVG grade: {best_student.avg_grade}"
        )


def select_3(subject_name):
    avg_grades = (
        session.query(
            Subject.name.label("subject_name"),
            Group.name.label("group_name"),
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .filter(Subject.name == subject_name)
        .group_by(Subject.name, Group.name)
        .all()
    )

    for subject_name, group_name, avg_grade in avg_grades:
        print(f"AVG grade in {subject_name} in {group_name}: {avg_grade}")


def select_4():
    avg_grade = session.query(
        func.round(func.avg(Grade.grade), 1).label("avg_grade")
    ).scalar()
    print(f"AVG grade: {avg_grade}")


def select_5(teacher_id):
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher:
        print(f"Teacher {teacher.first_name} {teacher.last_name} teachers:")
        if len(teacher.subjects) > 0:
            for subject in teacher.subjects:
                print(subject.name)
        else:
            print(f"Nothing")


def select_6(group_name):
    list_of_students = (
        session.query(Student.id, Student.first_name, Student.last_name)
        .join(Group)
        .filter(Group.name == group_name)
        .all()
    )

    print(f"Students in {group_name}:")
    for student in list_of_students:
        print(f"id {student.id}: {student.first_name} {student.last_name}")


def select_7(group_name, subject_name):
    students = (
        session.query(
            Student.id,
            Student.first_name,
            Student.last_name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .group_by(Student.id)
        .all()
    )

    print(f"AVG grades for students in group {group_name} for subject {subject_name}:")
    if students:
        for student in students:
            print(f"{student.first_name} {student.last_name}: {student.avg_grade}")

    else:
        return


def select_8():
    pass


def select_9():
    pass


def select_10():
    pass


def getRandomSubject():
    subject = session.query(Subject.name).distinct().all()
    if subject:
        random_subject = random.choice(subject)[0]
        return random_subject
    else:
        return


def getRandomTeacher():
    teacher = session.query(Teacher.id).distinct().all()
    if teacher:
        random_teacher = random.choice(teacher)[0]
        return random_teacher
    else:
        return


def getRandomGroupName():
    group = session.query(Group.name).distinct().all()
    if group:
        random_group = random.choice(group)[0]
        return random_group
    else:
        return


if __name__ == "__main__":
    with engine.connect() as connection:
        print(f"-------------------------------------------------------")
        print("")

        select_1()
        print(f"-------------------------------------------------------")
        print("")

        subject_name = getRandomSubject()
        if subject_name:

            select_2(subject_name)
            print(f"-------------------------------------------------------")
            print("")

            select_3(subject_name)
            print(f"-------------------------------------------------------")
            print("")

        select_4()
        print(f"-------------------------------------------------------")
        print("")

        teacher_name = getRandomTeacher()
        if teacher_name:
            select_5(teacher_name)
        print(f"-------------------------------------------------------")
        print("")

        group_name = getRandomGroupName()
        if group_name:
            select_6(group_name)
        print(f"-------------------------------------------------------")
        print("")

        if group_name and subject_name:
            select_7(group_name, subject_name)

        # if teacher_name:
        #     select_8(teacher_name)

        # student_name = getRandomStudent()
        # if student_name:
        #     select_9(student_name)

        # if student_name and teacher_name:
        #     select_10(student_name, teacher_name)
