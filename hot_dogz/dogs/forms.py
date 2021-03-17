from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from hot_dogz.models import Breed


class UploadForm(FlaskForm):
    name = StringField("Dog's name",
                       validators=[DataRequired()])
    img_url = FileField("Photo",
                        validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    breed = SelectField("Breed",
                        choices=[(breed.pk, breed.breed_name) for breed in Breed.objects],
                        validators=[DataRequired()])
    about = TextAreaField("Tell us about your dog!")
    submit = SubmitField('Upload')


class EditForm(FlaskForm):
    name = StringField("Dog's name",
                       validators=[DataRequired()])
    img_url = FileField("Photo",
                        validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    breed = SelectField("Breed",
                        choices=[(breed.pk, breed.breed_name) for breed in Breed.objects],
                        validators=[DataRequired()])
    about = TextAreaField("Tell us about your dog!")
    submit = SubmitField('Submit')


class CommentInput(FlaskForm):
    content = TextAreaField(validators=[DataRequired('Please enter a comment first!')])
    submit = SubmitField('Submit')