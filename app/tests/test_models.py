import pytest

from app import db, create_app
from app.learning_management_system.models import Teacher, Student

@pytest.fixture(scope='module')
def students():
	create_app()
	students = []
	data = [{'email': 'student1@foo.com'},
			{'email': 'student2@foo.com'},
			{'email': 'student3@foo.com'},]
	for row in data:
		students.append(Student(**row))
	
	yield students
	
	for student in students:
		db.session.delete(student)
	db.session.commit()

@pytest.fixture(scope='module')
def teachers():
	create_app()
	teachers = []
	data = [{'email': 'teacher1@foo.com'},
			{'email': 'teacher2@foo.com'},
			{'email': 'teacher3@foo.com'},]
	for row in data:
		teachers.append(Teacher(**row))
	
	yield teachers
	
	for teacher in teachers:
		db.session.delete(teacher)
	db.session.commit()

def test_insert_students(students):
	db.session.add_all(students)
	db.session.commit()

def test_insert_teachers(teachers):
	db.session.add_all(teachers)
	db.session.commit()