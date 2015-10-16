'''
configurations for flask app
'''

# temp login details
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'uni_of_nottingham'
THREADED = False
DEBUG = False

# port needs to be defined if we want to run in Vagrant
PORT = 8080
IP = "192.168.99.101"
