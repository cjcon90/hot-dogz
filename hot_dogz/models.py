from hot_dogz import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hot_dogz import login
import datetime
from cloudinary import api, uploader, utils, CloudinaryImage
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

    def set_avatar(self, img_url):
        self.img_url = img_url


class Breed(db.Document):
    breed_name = db.StringField(required=True)


class Dog(db.Document):
    name = db.StringField(required=True)
    img_url = db.URLField()
    img_url_thumb = db.URLField()
    owner = db.ReferenceField(User)
    breed = db.ReferenceField(Breed)
    about = db.StringField(default="No info on this doggo yet!")
    liked_by = db.ListField(db.ReferenceField(User))
    likes = db.IntField()
    faved_by = db.ListField(db.ReferenceField(User))
    upload_date = db.DateTimeField(default=datetime.datetime.utcnow)

    def set_dog_image(self, dog_img, user, pk):
        # Get an individual folder for each user's dog uploads
        public_id = f"hot_dogz/{user}/{pk}"
        # upload image to identified folder with eager transformations for smaller image
        res = uploader.upload(dog_img, public_id=public_id, eager = [{"width": 500, "crop": "scale", "quality": "auto:low"}], overwrite=True)
        # Get already configurated cloud name
        cloud_name = os.environ.get("CLOUD_NAME")
        # add to URL for building URL
        endpoint = f"https://res.cloudinary.com/{cloud_name}/image/upload"
        # Add transformations for delivering lower quality, smaller thumbnails
        transformation = '/w_500,c_scale,q_auto:low'
        # Get the version, id and format details from uploaded image
        version = f"/v{res['version']}/"
        public_id = res["public_id"]
        image_format = res["format"]
        # add links for full quality image and thumbnails to Dog model
        self.img_url = f"{endpoint}{version}{public_id}.{image_format}"
        self.img_url_thumb = f"{endpoint}{transformation}{version}{public_id}.{image_format}"
        


class Comment(db.Document):
    author = db.ReferenceField(User)
    dog = db.ReferenceField(Dog)
    content = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.datetime.utcnow)


class Favourite(db.Document):
    user = db.ReferenceField(User)
    dog = db.ReferenceField(Dog)

# Load the user from the database for flask-login
@login.user_loader
def load_user(id):
    return User.objects.get(pk=id)