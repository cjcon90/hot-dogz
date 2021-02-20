from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Document):
    username = db.StringField(required=True)
    email = db.EmailField(required=True)
    password_hash = db.StringField(required=True)
    img_url = db.URLField()


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            '_id': str(self.pk),
            'username': self.username,
            'email': self.email,
            'password': self.password_hash,
            'img_url': self.img_url
        }

# Load the user from the database for flask-login
@login.user_loader
def load_user(id):
    return User.objects.get(pk=id)