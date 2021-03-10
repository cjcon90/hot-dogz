import os
import cloudinary

# I used python-dotenv library to automatically import configs from a .flaskenv file in root folder when working locally
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
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['hotdogzapp@gmail.com', 'cjcon90@pm.me']