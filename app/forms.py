from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User, Breed


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="I'm gonna need your email"), Email(message="Are you sure this is an email?")])
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


class UploadForm(FlaskForm):
    name = StringField("Dog's name", validators=[DataRequired()])
    img_url = FileField("Photo", validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    breed = SelectField("Breed", choices=[(breed.pk, breed.breed_name) for breed in Breed.objects], validators=[DataRequired()])
    about = TextAreaField("Tell us about your dog!")
    submit = SubmitField('Upload')



