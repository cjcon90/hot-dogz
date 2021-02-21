from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from mongoengine.errors import DoesNotExist
from app import app
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
@login_required
def gallery():
    return render_template('gallery.html', title="Gallery")


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('gallery'))
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        login_user(user)
        flash("Registered! Please choose an avatar")
        return redirect(url_for('select_avatar'))
    return render_template('register.html', title="Register", form=form)


@app.route('/select_avatar')
@login_required
def select_avatar():
    if request.args.get('selected'):
        user = User.objects.get(username=current_user.username)
        user.set_avatar(request.args.get('selected'))
        user.save()
        flash('Your avatar has been updated!')
        return redirect(url_for('gallery'))
    avatars = [f'https://res.cloudinary.com/cjcon90/image/upload/v1613871615/codeinstitute/hot_dogz/dog_avatars/dog{i}.jpg' for i in range(1,17)]
    return render_template('select_avatar.html', avatars=avatars, title='Choose Avatar')
