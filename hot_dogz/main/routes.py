from flask import render_template, redirect, url_for, Blueprint, request
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
        return redirect(url_for('main.gallery', view='hot'))
    return render_template('index.html')

@main.route('/gallery/<view>')
def gallery(view):
    """
    Route for main gallery page with sections to
    display dogs sorted and filtered by:
    Hot: most liked dogs uploaded recently
    New: The most recently uploaded dogs
    Top: The dogs will the all time highest likes
    """
    page = request.args.get("page", 1, type=int)
    if view == 'hot':
        dogs = Dog.objects.order_by('-likes').paginate(page=page, per_page=1)
    elif view == 'new':
        dogs = Dog.objects.order_by('-upload_date').paginate(page=page, per_page=1)
    return render_template('gallery.html', title="Gallery", dogs=dogs, view=view)