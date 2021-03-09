from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please enter a username")])
    email = StringField('Email', validators=[DataRequired(message="Please enter an email"), Email(message="Please enter a valid email address")])
    message = TextAreaField("What can we help you with?", validators=[DataRequired(message="Please enter a message")])
    submit = SubmitField('Submit')