from flask import render_template, redirect, url_for, Blueprint, request, flash
from flask_login import current_user
from hot_dogz.models import Dog
from hot_dogz.main.forms import ContactForm
from hot_dogz.main.utils import send_email

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Route for initial landing page for
    users not yet logged in to the app
    """
    if current_user.is_authenticated:
        # redirect users to main page if they are already registered
        return redirect(url_for('main.gallery', view='hot', animate='on'))
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
        dogs = Dog.objects.order_by('-likes').paginate(page=page, per_page=5)
    elif view == 'new':
        dogs = Dog.objects.order_by('-upload_date').paginate(page=page, per_page=5)
    animate = request.args.get('animate')
    return render_template('gallery.html', title="Gallery", dogs=dogs, view=view, animate=animate)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash("Thank you! Your message has been sent", "check-circle")
        return redirect(url_for('main.gallery', view='hot'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('contact.html', form=form)