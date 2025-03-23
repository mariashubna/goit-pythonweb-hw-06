from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table,
    Column,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


association_table = Table(
    "association",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE")),
    Column("subject_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("student_id", "subject_id"),
)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    subjects: Mapped[list["Subject"]] = relationship(
        "Subject", secondary="association", back_populates="students"
    )
    group: Mapped["Group"] = relationship("Group", back_populates="students")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    students: Mapped[list["Student"]] = relationship("Student", back_populates="group")


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))

    subjects: Mapped[list["Subject"]] = relationship(
        "Subject", back_populates="teacher"
    )


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))

    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")
    students: Mapped[list["Student"]] = relationship(
        "Student", secondary="association", back_populates="subjects"
    )
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    grade: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    student: Mapped["Student"] = relationship("Student", back_populates="grades")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="grades")
