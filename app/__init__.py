from flask import Flask, session
from flask_mysqldb import MySQL
from config import Config
import MySQLdb

app = Flask(__name__)
app.config.from_object(Config)

host = 'localhost'
user = 'root'
password = 'csciGroup10!'
database = 'AgroAIDB'

session['loggedin'] = None
mysql_connection = get_mysql_connection()

    
from app import web