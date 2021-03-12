from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from config import Config
from flask_mail import Mail



db = MongoEngine()
login = LoginManager()
# configure view and message when users attemp to access a
# view for which @login_required
login.login_view = 'users.login'
login.login_message = 'You must be logged in to do that!'
login.login_message_category = 'exclamation'
mail = Mail()


# From Flask docs: Factories & Extensions:
# "Using this design pattern, no application-specific state is stored on the extension object,
# so one extension object can be used for multiple apps."
def create_app(config_class=Config):
    app = Flask(__name__)

    # add config settings to flask app (from config.py)
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)


    from hot_dogz.users.routes import users
    from hot_dogz.dogs.routes import dogs
    from hot_dogz.main.routes import main
    from hot_dogz.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(dogs)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app