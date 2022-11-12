import os
import cloudinary
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    # Flask Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Mongo DB Settings
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGO_DBNAME'),
        'host': os.environ.get('MONGO_URI')
    }
    # Cloudinary API Settings
    cloudinary.config(
        cloud_name=os.environ.get("CLOUD_NAME"),
        api_key=os.environ.get("CLOUD_API_KEY"),
        api_secret=os.environ.get("CLOUD_API_SECRET")
    )
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['ciaran@cjcon90.dev']
