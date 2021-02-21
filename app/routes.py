from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from mongoengine.errors import DoesNotExist
from app import app
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from random import randint


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
@login_required
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
        flash(f"Hello {user.username}, have successfully Logged in")
        return redirect(url_for('index'))
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
        return redirect(url_for('gallery'))
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # Set a random avatar in case the user exits out of avatar select screen
        user.set_avatar(f'https://res.cloudinary.com/cjcon90/image/upload/v1613871615/codeinstitute/hot_dogz/dog_avatars/dog{randint(1,16)}.png')
        user.save()
        login_user(user)
        flash("Registered! Please choose an avatar")
        # Redirect to avatar select screen for manual select
        return redirect(url_for('select_avatar'))
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
    avatars = [f'https://res.cloudinary.com/cjcon90/image/upload/v1613871615/codeinstitute/hot_dogz/dog_avatars/dog{i}.png' for i in range(1,17)]
    return render_template('select_avatar.html', avatars=avatars, title='Choose Avatar')


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.objects.get(username=username)
    return render_template('profile.html', user=user)
