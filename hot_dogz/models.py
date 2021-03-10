from hot_dogz import db
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import CASCADE
from flask_login import UserMixin
from flask import current_app
from hot_dogz import login
from hot_dogz.main.utils import JSONEncoder, decoder
import datetime
from cloudinary import uploader
from time import time
import jwt
import json
import os


class User(UserMixin, db.Document):
    username = db.StringField(required=True)
    email = db.EmailField(required=True)
    password_hash = db.StringField(required=True)
    img_url = db.URLField()


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Reset password code courtesy of Miguel Grinberg:
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-email-support
    def get_reset_password_token(self, expires_in=600):
        # Return a time limited JWT token for emailing to users requesting reset
        id = JSONEncoder().encode(self.id)
        return jwt.encode(
            {'reset_password': id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')


    @staticmethod
    def verify_reset_password_token(token):
        # receive returned JWT token following user's clicking link in password
        # Verify and return correct user
        try:
            id = json.loads(jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password'], object_hook=decoder)
        except:
            return
        return User.objects(pk=id).first()


    def set_avatar(self, img_url):
        self.img_url = img_url


    def __repr__(self):
        return f"User('{self.username}','{self.email}')"



class Breed(db.Document):
    breed_name = db.StringField(required=True)

    def __repr__(self):
        return f"Breed('{self.breed_name}')"



class Dog(db.Document):
    name = db.StringField(required=True)
    img_url = db.URLField()
    img_url_card = db.URLField()
    img_url_thumb = db.URLField()
    owner = db.ReferenceField(User, reverse_delete_rule=CASCADE)
    breed = db.ReferenceField(Breed)
    about = db.StringField(default="No info on this doggo yet!")
    liked_by = db.ListField(db.ReferenceField(User))
    likes = db.IntField()
    faved_by = db.ListField(db.ReferenceField(User))
    upload_date = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Dog('{self.name}', owner = {self.owner.username})"

    def set_dog_image(self, dog_img, user, pk):
        # Get an individual folder for each user's dog uploads
        # and set filename to dog's primary key, so a new photo upload overwrites the old one
        public_id = f"hot_dogz/{user}/{pk}"
        # upload image to identified folder with eager transformations for smaller image
        res = uploader.upload(dog_img, public_id=public_id, overwrite=True)
        # Get already configurated cloud name
        cloud_name = os.environ.get("CLOUD_NAME")
        # add to URL for building URL
        endpoint = f"https://res.cloudinary.com/{cloud_name}/image/upload"
        # Add transformations for delivering lower quality, smaller version
        # for dog card and dog profile page respectively
        card_transformation = '/c_fill,g_auto,h_350,w_525,q_auto:low'
        thumb_transformation = '/w_500,c_scale,q_auto:low'
        # Get the version, id and format details from uploaded image
        version = f"/v{res['version']}/"
        public_id = res["public_id"]
        image_format = res["format"]
        # add links for full quality image and thumbnails to Dog model
        self.img_url = f"{endpoint}{version}{public_id}.{image_format}"
        self.img_url_card = f"{endpoint}{card_transformation}{version}{public_id}.{image_format}"
        self.img_url_thumb = f"{endpoint}{thumb_transformation}{version}{public_id}.{image_format}"

    def delete_dog_image(self, user, pk):
        public_id = f"hot_dogz/{user}/{pk}"
        uploader.destroy(public_id)
        


class Comment(db.Document):
    author = db.ReferenceField(User, reverse_delete_rule=CASCADE)
    dog = db.ReferenceField(Dog, reverse_delete_rule=CASCADE)
    content = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.content}', author = '{self.author.username}')"


class Favourite(db.Document):
    user = db.ReferenceField(User, reverse_delete_rule=CASCADE)
    dog = db.ReferenceField(Dog, reverse_delete_rule=CASCADE)

    def __repr__(self):
        return f"Favourite('{self.dog.name}', favourited by '{self.user.username}')"

# Load the user from the database for flask-login
@login.user_loader
def load_user(id):
    return User.objects.get(pk=id)