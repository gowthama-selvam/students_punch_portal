from flask import render_template, url_for, flash, redirect, request, send_file
from daily_punch import app, admin, db, conn
from daily_punch.forms import RegistrationForm, LoginForm, Morning_reportForm, Evening_reportForm, ExportForm
from daily_punch.models import User, Intime, Outtime
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
import pandas as pd
from PIL import Image
import re

def excel_gen(self):
        df = pd.read_sql_query(f"select * from {self}", conn)
        df.to_excel(f"{self}.xlsx")


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    real_time = datetime.now()
    now_time = real_time.strftime('%H:%M:%S')

    time_ = datetime.strptime('12:00:00', '%H:%M:%S')
    condi_time = time_.strftime('%H:%M:%S')


    if now_time <= condi_time:
        if current_user.is_authenticated:
            return redirect(url_for('morning'))
        
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user and user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('morning'))
                flash('You got logged in', 'success')
            
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        
    if now_time >= condi_time:
        if current_user.is_authenticated:
            return redirect(url_for('evening'))
        
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user and user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('evening'))
                flash('You got logged in', 'success')

            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/morning", methods=['GET', 'POST'])
@login_required
def morning():
    user = User()
    form = Morning_reportForm()

    real_time = datetime.now()
    now_time = real_time.strftime('%H:%M:%S')

    if form.validate_on_submit():

        punch = Intime(remarks=form.discription.data, student=current_user.username)
        db.session.add(punch)
        db.session.commit()

        flash(f'Your daily report got submitted. Your intime is {now_time}', 'success')

        return redirect(url_for('morning'))

    return render_template('morning.html', title="Home", form=form, current_user=current_user, now_time=now_time)

@app.route("/evening", methods=['GET', 'POST'])
@login_required
def evening():
    user = User()
    form = Evening_reportForm()

    real_time = datetime.now()
    now_time = real_time.strftime('%H:%M:%S')

    if form.validate_on_submit():

        punch = Outtime(remarks=form.discription.data, student=current_user.username)
        db.session.add(punch)
        db.session.commit()

        flash(f'Your daily report got submitted. Your outtime is {now_time}', 'success')
        return redirect(url_for('evening'))

    return render_template('evening.html', title="Home", form=form, current_user=current_user, now_time=now_time)

@app.route("/about")
def about():
    return render_template('about.html', title="about")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/test', methods=['GET', 'POST'])
def test():

    if request.method == 'POST':
        print(request.form.getlist('download_list'))   

    return render_template('test.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None or session.get('if_logged') is None:
            return redirect('/login',code=302)
        return f(*args, **kwargs)
    return decorated_function

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class Export(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            expolist = request.form.getlist('mychechbox')
            for data in expolist:
                excel_gen(data)
                path = f"../{data}.xlsx"
                return send_file(path, as_attachment=True)

        return self.render('admin/export.html')

class Exit(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('login'))

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Intime, db.session))
admin.add_view(MyModelView(Outtime, db.session))
admin.add_view(Export(name='Export'))
admin.add_view(Exit(name='Back ->'))