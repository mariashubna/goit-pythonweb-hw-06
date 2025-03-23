from connect import engine, Base, session
from models import Student, Group, Teacher, Subject, Grade
from faker import Faker
import random
from datetime import datetime


fake = Faker()

Base.metadata.create_all(engine)


session.query(Student).delete()
session.query(Teacher).delete()
session.query(Grade).delete()
session.query(Subject).delete()
session.query(Group).delete()
session.commit()


teachers = []
for _ in range(5):
    teacher = Teacher(first_name=fake.first_name(), last_name=fake.last_name())
    teachers.append(teacher)
session.add_all(teachers)
session.commit()


subjects = [
    Subject(name="Literature", teacher_id=random.choice(teachers).id),
    Subject(name="Mathematics", teacher_id=random.choice(teachers).id),
    Subject(name="English", teacher_id=random.choice(teachers).id),
    Subject(name="German", teacher_id=random.choice(teachers).id),
    Subject(name="History", teacher_id=random.choice(teachers).id),
    Subject(name="Biology", teacher_id=random.choice(teachers).id),
]
session.add_all(subjects)
session.commit()


groups = [Group(name="Group 1"), Group(name="Group 2"), Group(name="Group 3")]
session.add_all(groups)
session.commit()


students = []
for _ in range(45):
    student = Student(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        group_id=random.choice(groups).id,
    )
    students.append(student)
session.add_all(students)
session.commit()


for student in students:
    student.subjects.extend(random.sample(subjects, k=4))

session.commit()


grades = []
for student in students:
    for subject in student.subjects:
        # число оцінок для конкретного предмета у студента
        num_grades = random.randint(3, 5)
        for _ in range(num_grades):
            # Генеруєм оцінку
            grade_value = random.randint(1, 12)
            # Генеруєм дату за останній рік
            grade_date = fake.date_time_between(start_date="-1y", end_date="now")
            grade = Grade(
                student_id=student.id,
                subject_id=subject.id,
                grade=grade_value,
                date=grade_date,
            )
            grades.append(grade)
session.add_all(grades)
session.commit()

session.close()


print(f"Teachers: {session.query(Teacher).count()}")
print(f"Groups: {session.query(Group).count()}")
print(f"Subjects: {session.query(Subject).count()}")
print(f"Students: {session.query(Student).count()}")
print(f"Grades: {session.query(Grade).count()}")
