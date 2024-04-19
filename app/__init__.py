from flask import Flask
from config import Config
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

try:
    connection = mysql.connect()
    print("MySQL connection:", connection)
except Exception as e:
    print("Error connecting to MySQL:", e)

from app import web