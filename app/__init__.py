from flask import Flask
from config import Config
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

print("MySQL object initialized:", mysql)
print("MySQL connection:", mysql.connection)


from app import web