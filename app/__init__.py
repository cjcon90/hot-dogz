from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from config import Config


app = Flask(__name__)
# add config settings to flask app (from config.py)
app.config.from_object(Config)
db = MongoEngine(app)
login = LoginManager(app)
login.login_view = 'login' # for @login_required decorator


from app import routes, models, errors
# import is below initialisation to avoid circular imports
# source: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world