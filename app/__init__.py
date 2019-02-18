import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(cfg='config.cfg'):
	app = Flask(__name__)
	app.config.from_pyfile(cfg)
	app.app_context().push()

	db.init_app(app)

	@app.errorhandler(404)
	def not_found(error):
	    return 'Error 404: Not found'

	from app.learning_management_system.controllers import learning_management_system as lms
	app.register_blueprint(lms)

	db.create_all()

	return app