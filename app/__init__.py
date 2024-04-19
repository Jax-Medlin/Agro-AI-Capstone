from flask import Flask
from flask_mysqldb import MySQL
from config import Config
import MySQLdb

app = Flask(__name__)
app.config.from_object(Config)

host = 'localhost'
user = 'root'
password = 'csciGroup10!'
database = 'AgroAIDB'

def get_mysql_connection():
    try:
        # Attempt to establish a MySQL connection
        connection = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
        print("MySQL connection successful!")
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
from app import web