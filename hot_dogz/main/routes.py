from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user
from hot_dogz.models import Dog

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Route for initial landing page for
    users not yet logged in to the app
    """
    if current_user.is_authenticated:
        # redirect users to main page if they are already registered
        return redirect(url_for('main.gallery'))
    return render_template('index.html')

@main.route('/gallery')
def gallery():
    """
    Route for main gallery page with sections to
    display dogs sorted and filtered by:
    Hot: most liked dogs uploaded recently
    New: The most recently uploaded dogs
    Top: The dogs will the all time highest likes
    """
    dogs = Dog.objects.order_by('-likes')
    return render_template('gallery.html', title="Gallery", dogs=dogs)