import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    MYSQLHOST = 'localhost'
    MYSQLUSER = 'root'
    MYSQLPASSWORD= 'csciGroup10!'
    MYSQLDB= 'AgroAIDB'