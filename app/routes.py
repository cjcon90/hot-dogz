from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from mongoengine.errors import DoesNotExist
from app import app
from app.forms import LoginForm, RegisterForm, UploadForm
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.models import User, Dog
from random import randint


@app.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        # redirect users to main page if they are already registered
        return redirect(url_for('gallery'))
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', title="Gallery")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """route for logging in users"""
    if current_user.is_authenticated:
        return redirect(url_for('gallery'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Used try/except, as mongoengine objects.get() returns DoesNotExist error if document doesn't exist
        try:
            user = User.objects.get(email=form.email.data)
        except DoesNotExist:
            user = None
        # If user doesn't exist or password doesn't match, notify user and reload page
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # else login the user and redirect
        login_user(user)
        flash(f"Welcome back, {user.username}!")
        next_page = request.args.get('next')
        # If the user had pressed to go to a page behind a @login_required
        # Then redirect to that 'next' page, otherwise go to main gallery
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('gallery')
        return redirect(next_page)
    # 'GET' functioning
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    """route to log out current user"""
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    """route for registering new users"""
    if current_user.is_authenticated:
        # redirect users to main page if they are already registered
        return redirect(url_for('gallery'))
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # Set a random avatar in case the user exits out of avatar select screen
        user.set_avatar(f'https://res.cloudinary.com/cjcon90/image/upload/v1613912365/hot_dogz/avatars/dog{randint(1,16)}.png')
        user.save()
        login_user(user)
        flash("Registered! Please choose an avatar")
        # Redirect to avatar select screen for manual select
        return redirect(url_for('select_avatar'))
    # 'GET' functioning
    return render_template('register.html', title="Register", form=form)


@app.route('/select_avatar')
@login_required
def select_avatar():
    """route for selecting avatar for new users
        or editing avatar for current users"""
    if request.args.get('selected'):
        user = User.objects.get(username=current_user.username)
        user.set_avatar(request.args.get('selected'))
        user.save()
        flash('Your avatar has been updated!')
        return redirect(url_for('profile', username=current_user.username))
    avatars = [f'https://res.cloudinary.com/cjcon90/image/upload/v1613912365/hot_dogz/avatars/dog{i}.png' for i in range(1,17)]
    return render_template('select_avatar.html', avatars=avatars, title='Choose Avatar')


@app.route('/profile/<username>')
def profile(username):
    user = User.objects(username=username).first_or_404()
    user_dogs = Dog.objects(owner=user)
    return render_template('profile.html', title=f"{user.username}", user=user, user_dogs=user_dogs)



@app.route('/upload_dog', methods = ['GET', 'POST'])
@login_required
def upload_dog():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        dog = Dog(name=form.name.data, owner=current_user.id, breed=form.breed.data,about=form.about.data)
        dog.set_user_image(form.img_url.data, current_user.username)
        dog.save()
        flash('Dog Uploaded!')
        return redirect(url_for('profile', username=current_user.username))
    # 'GET' functioning
    return render_template('upload_dog.html', form=form, title="Upload Dog")


@app.route('/dog/<dog_id>')
def dog_page(dog_id):
    dog = Dog.objects(pk=dog_id).first()
    return render_template('dog_page.html', dog=dog)

