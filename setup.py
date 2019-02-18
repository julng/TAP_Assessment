from setuptools import find_packages, setup

setup(
	name='learning_management_system',
	description = 'A system for teachers to perform administrative functions for their students.',
	author = 'Julian Ng',
	version='1.0.0',
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'flask', 'flask_sqlalchemy', 'flask_apispec', 'mysqlclient','requests'
	],
	# entry_points={
	# 	'console_scripts': [
	# 		'EducationSystem=app:run',
	# 	],
	# },
)

# setup(
#     py_modules=['app', 'db', 'db_config', 'models','resources'],
#     install_requires = [
#         'sqlalchemy','flask','flask-restful','flask-jsonpify'
#     ],
#     entry_points={
#         'console_scripts': [
#             'datasetmanager_server=app:run',
#         ],
#     },
	# setup_requires = [
	#     'pytest-runner',
	# ],
	# tests_require = [
	#     'pytest',
	# ],
# )