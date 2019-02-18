import json

from flask import Blueprint
from flask import request, abort, make_response
from flask_apispec import use_kwargs
from flask_sqlalchemy import orm

from sqlalchemy.sql import text

from marshmallow import fields

from app import db
from app.learning_management_system.models import Teacher, Student

learning_management_system = Blueprint('learning_management_system', __name__, url_prefix='/api')
session = db.session

@learning_management_system.route('/register', methods=['POST'])
@use_kwargs({'teacher': fields.Str(), 'students': fields.List(fields.Str())})
def register(teacher=None, students=None):
	'''Register one or more students to a specified teacher'''

	if not teacher or not students:
		return HTTP400('expected \'teacher\' and \'students\'')

	# check if exists
	t = session.query(Teacher).filter(Teacher.email==teacher).first()
	if not t:
		t = Teacher(email=teacher)
		session.add(t)
	
	for email in students:
		# check if exists
		s = session.query(Student).filter(Student.email==email).first()
		if not s:
			s = Student(email=email)
			session.add(s)

		# register students with teachers
		s.teachers.append(t)

	session.commit()

	return HTTP204()

@learning_management_system.route('/commonstudents', methods=['GET'])
@use_kwargs({'teacher': fields.List(fields.Str())})
def commonstudents(teacher=None):
	'''Get students registered to all of the given teachers'''

	if not teacher:
		return HTTP400('Bad Request Error: expected \'teacher\'')
	query = text('SELECT DISTINCT email '
				'FROM user AS u1 '
				'WHERE NOT EXISTS '
					'(SELECT * FROM user AS u2 '
				    'WHERE NOT EXISTS '
						'(SELECT * FROM registrations AS r '
				        'WHERE (u1.id = r.student_id) '
				        'AND (r.teacher_id = u2.id)) '
				        'AND (u2.email IN :emails))')
	results = db.engine.execute(query, emails=teacher)
	student_emails = [row[0] for row in results]
	response = {'students': student_emails}

	return HTTP200(json.dumps(response))

@learning_management_system.route('/suspend', methods=['POST'])
@use_kwargs({'student': fields.Str()})
def suspend(student=None):
	'''Suspend a student'''

	if not student:
		return HTTP400('expected \'student\'')

	# check if exists
	s = session.query(Student).filter(Student.email==student).first()
	if not s:
		return HTTP400('student %s does not exist' % student)
	
	s.suspended = True
	session.commit()

	return HTTP204()

@learning_management_system.route('/retrievefornotifications', methods=['POST'])
@use_kwargs({'teacher': fields.Str(), 'notification': fields.Str()})
def retrievefornotifications(teacher=None, notification=None):
	'''Retrieve a list of students who can receive a given notification'''

	if not teacher or not notification:
		return HTTP400('expected \'teacher\' and \'notification\'')

	# check if exists
	t = session.query(Teacher).filter(Teacher.email==teacher).first()
	if not t:
		return HTTP400('teacher %s does not exist' % teacher)

	notification_list = notification.split()
	message = notification_list.pop(0)
	# remove @ char at the front of emails
	notification_list = [n[1:] for n in notification_list]

	students = session.query(Student).filter(Student.email.in_(notification_list)).all()
	# filter suspended students
	notification_list = {s.email for s in students if s.suspended==False}
	# combined list of unique emails
	notification_list = notification_list.union({s.email for s in t.students if s.suspended==False})
	recipients = {'recipients': list(notification_list)}

	return HTTP200(json.dumps(recipients))

def HTTP400(message):
	message = 'Bad Request Error: %s' % message
	status = 400
	return make_response(message, status)

def HTTP204():
	return make_response('', 204)

def HTTP200(message):
	status = 200
	return make_response(message, status)