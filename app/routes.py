from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
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
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.objects.get(email=form.email.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        flash(f"Hello {user.username}, have successfully Logged in")
        return redirect(url_for('index'))
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("You have successfully registered")
        return redirect(url_for('index'))
    return render_template('register.html', title="Register", form=form)
