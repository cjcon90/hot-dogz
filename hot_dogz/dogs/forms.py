from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from hot_dogz.models import Breed


class UploadForm(FlaskForm):
    name = StringField("Dog's name",
                       validators=[DataRequired(),
                                   Length(max=20,
                                          message="Max name length is 20 characters! Does your dog have a nickname?")])
    img_url = FileField("Photo",
                        validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    breed = SelectField("Breed",
                        choices=[(breed.pk, breed.breed_name) for breed in Breed.objects],
                        validators=[DataRequired()])
    about = TextAreaField("Tell us about your dog!",
                          validators=[Length(max=250,
                                             message="About section has a max character limit of 250!")])
    submit = SubmitField('Upload')


class EditForm(FlaskForm):
    name = StringField("Dog's name",
                       validators=[DataRequired()])
    img_url = FileField("Photo",
                        validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    breed = SelectField("Breed",
                        choices=[(breed.pk, breed.breed_name) for breed in Breed.objects],
                        validators=[DataRequired()])
    about = TextAreaField("Tell us about your dog!",
                          validators=[Length(max=250,
                                             message="About section has a max character limit of 250!")])
    submit = SubmitField('Submit')


class CommentInput(FlaskForm):
    content = TextAreaField(
        validators=[DataRequired('Please enter a comment first!'),
                    Length(max=250, message="Comments have a max character limit of 250!")])
    submit = SubmitField('Submit')
