from mongoengine.fields import DateTimeField, StringField, ReferenceField, EmailField, URLField
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import datetime


class User(UserMixin, db.Document):
    username = db.StringField(required=True)
    email = db.EmailField(required=True)
    password_hash = db.StringField(required=True)
    img_url = db.URLField()


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_avatar(self, img_url):
        self.img_url = img_url


class Breed(db.Document):
    breed_name = db.StringField(required=True)


class Dog(db.Document):
    name = db.StringField(required=True)
    img_url = db.URLField(required=True)
    owner = db.ReferenceField(User)
    breed = db.ReferenceField(Breed)
    about = db.StringField(default="No info on this doggo yet!")
    upload_date = db.DateTimeField(default=datetime.datetime.utcnow)


# Load the user from the database for flask-login
@login.user_loader
def load_user(id):
    return User.objects.get(pk=id)