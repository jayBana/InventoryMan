__author__ = 'janosbana'

'''
configs for Flask app
'''

import os

# basedir
basedir = os.path.abspath(os.path.dirname(__file__))

# temp login details
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'uni_of_nottingham'

# port needs to be defined if it want it to run in vagrant
PORT = 8080