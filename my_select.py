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
            print(
                f"Id {student.id}: {student.first_name} {student.last_name}: {student.avg_grade}"
            )

    else:
        return


def select_8(teacher_id):
    avg_grade = (
        session.query(
            Subject.name.label("subject_name"),
            Teacher.first_name.label("first_name"),
            Teacher.last_name.label("last_name"),
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.id == teacher_id)
        .group_by(Subject.name, Teacher.id)
        .all()
    )

    if avg_grade:
        teacher = avg_grade[0]
        print(
            f"AVG grade from teacher {teacher.first_name} {teacher.last_name} with ID {teacher_id} for subjects:"
        )

        for subject in avg_grade:
            print(f"{subject.subject_name}: {subject.avg_grade}")
    else:
        print(
            f"Teacher with ID {teacher_id} has no grades or does not teach any subjects."
        )


def select_9(student_id):
    courses = (
        session.query(Subject.name, Student.first_name, Student.last_name)
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Student.id == student_id)
        .distinct()
        .all()
    )

    student = courses[0]

    if courses:
        print(
            f"Courses for student {student.first_name} {student.last_name} with ID {student_id}:"
        )
        for course in courses:
            print(course.name)
    else:
        print(f"Student with ID {student_id} is not enrolled in any courses.")


def select_10(student_id, teacher_id):
    courses = (
        session.query(
            Subject.name,
            Student.first_name,
            Student.last_name,
            Teacher.first_name.label("teacher_first_name"),
            Teacher.last_name.label("teacher_last_name"),
        )
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Student, Student.id == Grade.student_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Student.id == student_id, Teacher.id == teacher_id)
        .distinct()
        .all()
    )

    if courses:
        student_name = f"{courses[0].first_name} {courses[0].last_name}"
        teacher_name = f"{courses[0].teacher_first_name} {courses[0].teacher_last_name}"
        print(
            f"Courses taught by teacher {teacher_name} with ID {teacher_id} to student {student_name} with ID {student_id} :"
        )
        for course in courses:
            print(course.name)
    else:
        print(
            f"No courses found for student with ID {student_id} and teacher with ID {teacher_id}."
        )


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


def getRandomStudent():
    student = session.query(Student.id).distinct().all()
    if student:
        random_student = random.choice(student)[0]
        return random_student
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

        teacher_id = getRandomTeacher()
        if teacher_id:
            select_5(teacher_id)
        print(f"-------------------------------------------------------")
        print("")

        group_name = getRandomGroupName()
        if group_name:
            select_6(group_name)
        print(f"-------------------------------------------------------")
        print("")

        if group_name and subject_name:
            select_7(group_name, subject_name)
        print(f"-------------------------------------------------------")
        print("")

        if teacher_id:
            select_8(teacher_id)
        print(f"-------------------------------------------------------")
        print("")

        student_id = getRandomStudent()
        if student_id:
            select_9(student_id)
        print(f"-------------------------------------------------------")
        print("")

        if student_id and teacher_id:
            select_10(student_id, teacher_id)
        print(f"-------------------------------------------------------")
        print("")
