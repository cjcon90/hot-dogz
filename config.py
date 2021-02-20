import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGO_DBNAME'),
        'host': os.environ.get('MONGO_URI')
    }