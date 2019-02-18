import pytest
import json

from app import db, create_app
from app.learning_management_system.models import Teacher, Student, User, registrations

@pytest.fixture(scope='module')
def client(teacher_email, student_email):
	app = create_app()
	client = app.test_client()

	yield client

	# delete test data
	stmt = User.__table__.delete().\
		where(Teacher.id == registrations.c.teacher_id).\
		where(registrations.c.student_id == Student.id).\
		where(User.email.in_(teacher_email+student_email))
	db.engine.execute(stmt)
	
@pytest.fixture(scope='module')
def teacher_email():
	teacher_email = ['teacherken@gmail.com', 'teacherben@gmail.com']
	return teacher_email

@pytest.fixture(scope='module')
def student_email():
	student_email = ['studentjon@example.com', 'studenthon@example.com']
	return student_email

@pytest.fixture(scope='module')
def invalid_student_email():
	invalid_student_email = 'student@notexist.com'
	return invalid_student_email

def test_register(client, teacher_email, student_email):
	rv = client.post('/api/register',
					json = {'teacher': teacher_email[0],
						  	'students': student_email})
	assert rv.status_code == 204

	t = db.session.query(Teacher).filter(Teacher.email==teacher_email[0]).first()
	assert set(student_email) == {s.email for s in t.students}
	
	rv = client.post('/api/register',
					json = {'teacher': teacher_email[1],
						  	'students': student_email})
	assert rv.status_code == 204

	s = db.session.query(Student).filter(Student.email==student_email[0]).first()
	assert set(teacher_email) == {t.email for t in s.teachers}

def test_register_wrong_format(client, teacher_email, student_email):
	rv = client.post('/api/register',
					json = {'teacher': 1,
						  	'students': 2})
	assert rv.status_code == 422

	rv = client.post('/api/register',
					json = {'foo': teacher_email[0],
						  	'bar': student_email})
	assert rv.status_code == 400

def test_suspend(client, student_email, invalid_student_email):
	s = db.session.query(Student).filter(Student.email==student_email[0]).first()
	assert s.suspended == False

	rv = client.post('/api/suspend',
					json = {'student': student_email[0]})
	assert rv.status_code == 204

	s = db.session.query(Student).filter(Student.email==student_email[0]).first()
	assert s.suspended == True

	rv = client.post('/api/suspend',
					json = {'student': invalid_student_email})
	assert rv.status_code == 400



def test_retrievefornotifications(client, teacher_email, student_email):
	t = db.session.query(Teacher).filter(Teacher.email==teacher_email[0]).first()
	notification = 'message @' + ' @'.join(student_email)
	rv = client.post('/api/retrievefornotifications',
					json = {'teacher': teacher_email[0],
						  	'notification': notification})
	assert rv.status_code == 200