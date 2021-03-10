from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login.utils import login_required
from jwt import MissingRequiredClaimError
from mongoengine.errors import DoesNotExist
from hot_dogz.users.forms import LoginForm, RegisterForm, EditProfileForm, RequestPasswordForm, ResetPasswordForm, DeleteAccountForm
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from hot_dogz.models import User, Dog
from hot_dogz.users.utils import send_password_reset_email, deanimate
from random import randint

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    """route for logging in users"""
    if current_user.is_authenticated:
        return redirect(url_for('main.gallery', view='hot', animate='on'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Used try/except, as mongoengine objects.get() returns DoesNotExist error if document doesn't exist
        try:
            user = User.objects.get(username=form.username.data.lower())
        except DoesNotExist:
            user = None
        # If user doesn't exist or password doesn't match, notify user and reload page
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'exclamation')
            return redirect(url_for('users.login'))
        # else login the user and redirect
        login_user(user)
        flash(f"Welcome back, {user.username}!", 'check-circle')
        next_page = request.args.get('next')
        # If the user had pressed to go to a page behind a @login_required
        # Then redirect to that 'next' page, otherwise go to main gallery
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.gallery', view='hot', animate='on')
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
        return redirect(url_for('main.gallery', view='hot', animate='on'))
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data)
        user.set_password(form.password.data)
        # Set a random avatar in case the user exits out of avatar select screen
        user.set_avatar(f'https://res.cloudinary.com/cjcon90/image/upload/v1613912365/hot_dogz/avatars/dog{randint(1,16)}.png')
        user.save()
        login_user(user)
        flash("Registered! Please choose an avatar", 'check-circle')
        # Redirect to avatar select screen for manual select
        return redirect(url_for('users.select_avatar'))
    # 'GET' functioning
    return render_template('register.html', title="Register", form=form)


@users.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Route for requesting a password Reset"""
    if current_user.is_authenticated:
        return redirect(url_for('main.gallery', view='hot'))
    form = RequestPasswordForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password', 'check-circle')
        return redirect(url_for('users.login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Password reset form, if request and
    jwt token signing was successful"""
    if current_user.is_authenticated:
        return redirect(url_for('main.gallery', view='hot'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('users.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.save()
        flash('Your password has been reset.', 'check-circle')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form)


@users.route('/profile/<username>')
def profile(username):
    """
    Route for displaying a user's profile page
    displaying own dogs and favourite dogs
    """
    user = User.objects(username=username).first()
    user_dogs = Dog.objects(owner=user)
    favourites = Dog.objects(faved_by__contains=current_user.id)
    return render_template('profile.html', title=f"{user.username}", user=user, user_dogs=user_dogs, favourites=favourites)


@users.route('/select_avatar')
@login_required
def select_avatar():
    """route for selecting avatar for new users
        or editing avatar for current users"""
    
    #Fuctioning if user has selected a new avatar
    if request.args.get('selected'):
        user = User.objects.get(username=current_user.username)
        user.set_avatar(request.args.get('selected'))
        user.save()
        flash('Your avatar has been updated!', 'check-circle')
        return redirect(url_for('users.profile', username=current_user.username))
    #Default functioning to present available avatars
    avatars = [f'https://res.cloudinary.com/cjcon90/image/upload/v1613912365/hot_dogz/avatars/dog{i}.png' for i in range(1,17)]
    return render_template('select_avatar.html', avatars=avatars, title='Choose Avatar')


@users.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """route for editing username, email
    or password"""
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.save()
        flash('Account updated successfully!', 'check-circle')
        return redirect(url_for('users.profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@users.route('/delete_account/', methods=['GET', 'POST'])
@login_required
def delete_account():
    """route for editing username, email
    or password"""
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = User.objects(username=current_user.username).first()
        # Complete password check before deletion
        if not user.check_password(form.password.data):
            flash('Invalid Password', 'exclamation')
            return redirect(url_for('users.profile', username=current_user.username))
        else:
            #Logout user to home screen
            logout_user()
            # Delete stored cloudinary image for each of user's dogs
            dogs = Dog.objects(owner=user)
            for dog in dogs:
                dog.delete_dog_image(user.username, dog.pk)
            # Delete user (which will cascade delete dogs, comments, etc)
            user.delete()
            flash('Account deleted! Hope to see you again', 'check-circle')
            return redirect(url_for('main.index'))

    return render_template('delete_account.html', title='Delete Account', form=form)



@users.route('/like/<dog_id>')
def like(dog_id):
    """
    Route for liking a dog and increasing their
    like count
    """
    # Only allow registered users to like
    if current_user.is_anonymous:
        flash('You must be a registered user to do that!', 'exclamation')
        return deanimate(request.referrer)
    dog = Dog.objects(pk=dog_id).first_or_404()
    # Remove from likes if already liked
    if current_user in dog.liked_by:
        dog.update(pull__liked_by=current_user.id)
        dog.update(dec__likes=1)
    # lse add to likes
    else:
        dog.update(push__liked_by=current_user.id)
        dog.update(inc__likes=1)
        flash(f'"Thanks for the like!" ~ {dog.name}', 'thumbs-up')

    # Return to previous page ensuring no gallery animation
    return deanimate(request.referrer)


@users.route('/favourite/<dog_id>')
def favourite(dog_id):
    """
    Route for saving a dog to the current
    user's favourites
    """
    # Only allow registered users to favourite
    if current_user.is_anonymous:
        flash('You must be a registered user to do that!', 'exclamation')
        return deanimate(request.referrer)
    dog = Dog.objects(pk=dog_id).first_or_404()
    if dog.owner == current_user:
        flash(f"{dog.name} is already saved, they're yours!", 'heart')
        return deanimate(request.referrer)
    # Remove from favourites if already favourites
    elif current_user in dog.faved_by:
        dog.update(pull__faved_by=current_user.id)
    # else add to favourites
    else:
        dog.update(push__faved_by=current_user.id)
        flash(f"{dog.name} added to favourites!", 'heart')

    # Return to previous page ensuring no gallery animation
    return deanimate(request.referrer)
