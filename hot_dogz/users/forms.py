from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from hot_dogz.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="I'm gonna need your username")])
    password = PasswordField('Password', validators=[DataRequired(message="Can't let you in without a password!")])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="I need to know what to call you!")])
    email = StringField('Email', validators=[DataRequired(message="I'm gonna need your email"), Email(message="Are you sure this is an email?")])
    password = PasswordField('Password', validators=[DataRequired(message="Can't let you in without a password!")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(message="We gotta double check that password"), EqualTo('password', message="Passwords don't match! Try again")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing = User.objects(username=username.data).count()
        if existing:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        existing = User.objects(email=email.data).count()
        if existing:
            raise ValidationError('Please use a different email.')