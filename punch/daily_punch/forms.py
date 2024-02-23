from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, optional, length


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(),], render_kw={"placeholder":"Enter your email"})
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Morning_reportForm(FlaskForm):
    discription = TextAreaField('Remarks', [optional(), length(max=300)])
    submit = SubmitField('Submit')

class Evening_reportForm(FlaskForm):
    discription = TextAreaField('Remarks', [optional(), length(max=300)])
    submit = SubmitField('Submit')

class ExportForm(FlaskForm):
    submit = SubmitField('Export')