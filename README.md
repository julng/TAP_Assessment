TAP_Assessment
==============

This repository is for GovTech's Technology Associate Programme Assessment (Apps development).

Requirements
------------
- Python 2.7 or 3.4+
- virtualenv
- git (for cloning this repository)
- MySQL (with Python support)

Installation
------------

Clone the repository and install dependencies in a virtual environment:

    $ git clone https://github.com/julng/TAP_Assessment.git
    $ cd TAP_Assessment
    $ virtualenv venv
    $ . venv/bin/activate
    (venv) pip install -r requirements.txt

Windows users: replace `. venv/bin/activate` with `venv\Scripts\activate`

Starting the server
-----------------------

Login to MySQL with your credentials and execute the script located at `./schema.sql`. Configure your username and password in `./app/config.cfg`

Start the flask application:

	$ python run.py

The app will run on http://127.0.0.1:5000

Tests
------

Some basic tests are included. They do not cover every possible test case.
	
	$ pytest
