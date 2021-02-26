from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login.utils import login_required
from mongoengine.errors import DoesNotExist
from hot_dogz.users.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from hot_dogz.models import User, Dog, Favourite
from random import randint

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    """route for logging in users"""
    if current_user.is_authenticated:
        return redirect(url_for('main.gallery'))
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
            return redirect(url_for('users.login'))
        # else login the user and redirect
        login_user(user)
        flash(f"Welcome back, {user.username}!")
        next_page = request.args.get('next')
        # If the user had pressed to go to a page behind a @login_required
        # Then redirect to that 'next' page, otherwise go to main gallery
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.gallery')
        return redirect(next_page)
    # 'GET' functioning
    return render_template('login.html', title="Login", form=form)


@users.route('/logout')
def logout():
    """route to log out current user"""
    logout_user()
    return redirect(url_for('main.index'))



@users.route('/register', methods=['GET', 'POST'])
def register():
    """route for registering new users"""
    if current_user.is_authenticated:
        # redirect users to main page if they are already registered
        return redirect(url_for('main.gallery'))
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
        return redirect(url_for('users.select_avatar'))
    # 'GET' functioning
    return render_template('register.html', title="Register", form=form)

@users.route('/profile/<username>')
def profile(username):
    user = User.objects(username=username).first_or_404()
    user_dogs = Dog.objects(owner=user)
    favourites = Dog.objects(faved_by__contains=current_user.id)
    return render_template('profile.html', title=f"{user.username}", user=user, user_dogs=user_dogs, favourites=favourites)


@users.route('/select_avatar')
@login_required
def select_avatar():
    """route for selecting avatar for new users
        or editing avatar for current users"""
    if request.args.get('selected'):
        user = User.objects.get(username=current_user.username)
        user.set_avatar(request.args.get('selected'))
        user.save()
        flash('Your avatar has been updated!')
        return redirect(url_for('users.profile', username=current_user.username))
    avatars = [f'https://res.cloudinary.com/cjcon90/image/upload/v1613912365/hot_dogz/avatars/dog{i}.png' for i in range(1,17)]
    return render_template('select_avatar.html', avatars=avatars, title='Choose Avatar')


@users.route('/like/<dog_id>')
def like(dog_id):
    dog = Dog.objects(pk=dog_id).first_or_404()
    if current_user in dog.liked_by:
        dog.update(pull__liked_by=current_user.id)
    else:
        dog.update(push__liked_by=current_user.id)
    return redirect(request.referrer)


@users.route('/favourite/<dog_id>')
def favourite(dog_id):
    dog = Dog.objects(pk=dog_id).first_or_404()
    if current_user in dog.faved_by:
        dog.update(pull__faved_by=current_user.id)
    else:
        dog.update(push__faved_by=current_user.id)
    print()

    return redirect(request.referrer)