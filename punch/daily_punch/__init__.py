from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_datepicker import datepicker
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import pandas as pd
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
admin = Admin(app, template_mode='bootstrap4')
conn = sqlite3.connect('/var/www/html/punch/daily_punch/site.db', check_same_thread=False)

from daily_punch import routes
