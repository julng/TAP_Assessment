from app import db

# aliases
Column = db.Column
ForeignKey = db.ForeignKey
Table = db.Table
relationship = db.relationship
Integer = db.Integer
String = db.String
Boolean = db.Boolean

class Base(db.Model):

	__abstract__  = True

	id            = db.Column(db.Integer, primary_key=True)
	date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
										   onupdate=db.func.current_timestamp())

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	email = Column(String(120), unique=True, nullable=False)
	type = Column(String(50))

	__mapper_args__ = {
		'polymorphic_identity': 'user',
		'polymorphic_on': type
	}

class Teacher(User):
	__tablename__ = 'teacher'

	id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
	
	students = relationship('Student',
							secondary = 'registrations',
							back_populates = 'teachers')
	
	__mapper_args__ = {
		'polymorphic_identity':'teacher',
	}

	def __repr__(self):
		return self.email

class Student(User):
	__tablename__ = 'student'

	id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
	suspended = Column(Boolean, default = False)

	teachers = relationship('Teacher',
							secondary = 'registrations',
							back_populates = 'students')
	
	__mapper_args__ = {
		'polymorphic_identity':'student',
	}

	def __repr__(self):
		return self.email

registrations = Table('registrations',
	Column('teacher_id', Integer, ForeignKey('teacher.id', ondelete='CASCADE'), primary_key=True),
	Column('student_id', Integer, ForeignKey('student.id', ondelete='CASCADE'), primary_key=True)
)

# def run():
# 	from db_config import DB_URI
# 	from sqlalchemy import create_engine
# 	engine = create_engine(DB_URI)
# 	# Base.metadata.drop_all(engine)
# 	Base.metadata.create_all(engine)
# 	print('Schema created')

# if __name__ == '__main__':
# 	run()