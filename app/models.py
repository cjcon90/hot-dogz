from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import datetime
import cloudinary.api
import cloudinary.uploader
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
    img_url = db.URLField(required=True)
    owner = db.ReferenceField(User)
    breed = db.ReferenceField(Breed)
    about = db.StringField(default="No info on this doggo yet!")
    upload_date = db.DateTimeField(default=datetime.datetime.utcnow)

    def set_user_image(self, dog_img, user):
        # Get an individual folder for each user's dog uploads
        folder = f"hot_dogz/{user}/"
        # upload image to identified folder with Cloudinary image optimization
        res = cloudinary.uploader.upload(dog_img, folder=folder)
        # Get already configurated cloud name
        cloud_name = os.environ.get("CLOUD_NAME")
        # add to URL for building URL
        endpoint = f"https://res.cloudinary.com/{cloud_name}/image/upload"
        # Set the image automatically scaled to the maximum width available
        # auto optimize image quality
        # deliver in jpg
        transformation = '/f_jpg,w_auto,c_scale,q_auto:low'
        # Get the version, id and format details from uploaded image
        version = f"/v{res['version']}/"
        public_id = res["public_id"]
        image_format = res["format"]
        # compile above details to build full URL for uploaded image
        self.img_url = f"{endpoint}{transformation}{version}{public_id}.{image_format}"
        


# Load the user from the database for flask-login
@login.user_loader
def load_user(id):
    return User.objects.get(pk=id)