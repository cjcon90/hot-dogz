from flask import Flask


app = Flask(__name__)


from app import routes, models, errors
# import is below initialisation to avoid circular imports
# source: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world