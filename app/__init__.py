from flask import Flask
from config import Config


app = Flask(__name__)
# add config settings to flask app (from config.py)
app.config.from_object(Config)


from app import routes, models, errors
# import is below initialisation to avoid circular imports
# source: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world