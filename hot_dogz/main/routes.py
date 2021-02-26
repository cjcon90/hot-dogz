from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user
from hot_dogz.models import Dog

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        # redirect users to main page if they are already registered
        return redirect(url_for('main.gallery'))
    return render_template('index.html')

@main.route('/gallery')
def gallery():
    dogs = Dog.objects.order_by('-likes')
    return render_template('gallery.html', title="Gallery", dogs=dogs)