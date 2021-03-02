from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from hot_dogz.models import User
from flask_login import current_user

# Form for loggin in existing users
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please enter a username")])
    password = PasswordField('Password', validators=[DataRequired(message="Please enter a password")])
    submit = SubmitField('Sign In')


# Form for registering new users
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please enter a username")])
    email = StringField('Email', validators=[DataRequired(message="Please enter an email"), Email(message="Please enter a valid email address")])
    password = PasswordField('Password', validators=[DataRequired(message="Please enter a password")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(message="Please double check password"), EqualTo('password', message="Passwords don't match! Please try again")])
    submit = SubmitField('Register')

    # Function to check that username isn't already registered on site
    def validate_username(self, username):
        existing = User.objects(username=username.data).first()
        if existing is not None:
            raise ValidationError('Please use a different username.')

    # Function to check that email isn't already registered on site
    def validate_email(self, email):
        existing = User.objects(email=email.data).first()
        if existing is not None:
            raise ValidationError('Please use a different email.')


# Form for editing a user's username or email
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please enter a username")])
    email = StringField('Email', validators=[DataRequired(message="Please enter an email"), Email(message="Please enter a valid email address")])
    submit = SubmitField('Submit')

    # Function to check that username (if new) isn't already registered on site
    def validate_username(self, username):
        if username.data != current_user.username:
            existing = User.objects(username=username.data).first()
            if existing is not None:
                raise ValidationError('Please use a different username.')

    # Function to check that email (if new) isn't already registered on site
    def validate_email(self, email):
        if email.data != current_user.email:
            existing = User.objects(email=email.data).first()
            if existing is not None:
                raise ValidationError('Please use a different email.')