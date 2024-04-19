from flask import Flask
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

with app.app_context():
    try:
        connection = mysql.connection
        print("MySQL connection:", connection)
    except Exception as e:
        print("Error connecting to MySQL:", e)

from app import web