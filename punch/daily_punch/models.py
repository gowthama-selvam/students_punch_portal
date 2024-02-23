from datetime import datetime
from daily_punch import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    batch = db.Column(db.String(5), nullable=False, default='RP--')
    password = db.Column(db.String(60), nullable=False)
    student_id = db.Column(db.String(8), nullable=False, unique=True,)
    domain = db.Column(db.String(20), nullable=False, default='IMS')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')


class Intime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    remarks = db.Column(db.String(200))
    student = db.Column(db.String(30), nullable=False)

class Outtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outtime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    remarks = db.Column(db.String(200))
    student = db.Column(db.String(30), nullable=False)
