from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login.utils import login_required
from mongoengine.errors import DoesNotExist
from hot_dogz.users.forms import LoginForm, RegisterForm, EditProfileForm, \
    RequestPasswordForm, ResetPasswordForm, DeleteAccountForm
from hot_dogz.dogs.forms import CommentInput
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from hot_dogz.models import User, Dog, Comment
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
        # Used try/except, as mongoengine objects.get() returns DoesNotExist
        # error if document doesn't exist
        try:
            user = User.objects.get(username=form.username.data.lower())
        except DoesNotExist:
            user = None
        # If user doesn't exist or password doesn't match, notify user and
        # reload page
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
    return render_template('user/login.html', title="Login", form=form)


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
        # Set a random avatar in case the user exits out of avatar select
        # screen
        user.set_avatar(
            f'https://res.cloudinary.com/cjcon90/image/upload/v1613912365'
            f'/hot_dogz/avatars/dog{randint(1, 16)}.png')
        user.save()
        login_user(user)
        flash("Registered! Please choose an avatar", 'check-circle')
        # Redirect to avatar select screen for manual select
        return redirect(url_for('users.select_avatar'))
    # 'GET' functioning
    return render_template('user/register.html', title="Register", form=form)


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
        flash('Check your email for the instructions to reset your password',
              'check-circle')
        flash('(Remember to check your spam folder!)', 'comment')
        return redirect(url_for('users.login'))
    return render_template('user/reset_password_request.html',
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
    return render_template('user/reset_password.html', token=token, form=form)


@users.route('/profile/<username>')
def profile(username):
    """
    Route for displaying a user's profile page
    displaying own dogs and favourite dogs
    """
    user = User.objects(username=username).first()
    user_dogs = Dog.objects(owner=user)
    favourites = Dog.objects(faved_by__contains=user.id)
    return render_template('user/profile.html', title=f"{user.username}",
                           user=user, user_dogs=user_dogs,
                           favourites=favourites)


@users.route('/select_avatar')
@login_required
def select_avatar():
    """route for selecting avatar for new users
        or editing avatar for current users"""

    # Fuctioning if user has selected a new avatar
    if request.args.get('selected'):
        user = User.objects.get(username=current_user.username)
        user.set_avatar(request.args.get('selected'))
        user.save()
        flash('Your avatar has been updated!', 'check-circle')
        return redirect(
            url_for('users.profile', username=current_user.username))
    # Default functioning to present available avatars
    avatars = [
        f'https://res.cloudinary.com/cjcon90/image/upload/v1613912365'
        f'/hot_dogz/avatars/dog{i}.png'
        for i in range(1, 17)]
    return render_template('user/select_avatar.html', avatars=avatars,
                           title='Choose Avatar')


@users.route('/edit_profile/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    """route for editing username, email
    or password"""
    user = User.objects(pk=user_id).first()
    if user != current_user and current_user.username != 'admin':
        flash("You cannot edit someone else's profile!", "exclamation")
        return redirect(url_for('main.gallery', view='hot'))
    form = EditProfileForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.save()
        flash('Account updated successfully!', 'check-circle')
        return redirect(url_for('users.profile', username=user.username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    return render_template('user/edit_profile.html', title='Edit Profile',
                           user=user, form=form)


@users.route('/delete_account/<user_id>', methods=['GET', 'POST'])
@login_required
def delete_account(user_id):
    """route for editing username, email
    or password"""
    user = User.objects(pk=user_id).first()
    if user != current_user and current_user.username != 'admin':
        flash("You cannot delete someone else's profile!", "exclamation")
        return redirect(url_for('main.gallery', view='hot'))
    form = DeleteAccountForm()
    if form.validate_on_submit():
        # Complete password check before deletion (admin can enter admin
        # password)
        if not current_user.check_password(form.password.data):
            flash('Invalid Password', 'exclamation')
            return redirect(url_for('users.profile', username=user.username))
        else:
            if current_user.username != 'admin':
                # Logout user to home screen
                logout_user()
            # Delete stored cloudinary image for each of user's dogs
            dogs = Dog.objects(owner=user)
            for dog in dogs:
                dog.delete_dog_image(user.username, dog.pk)
            # Delete user (which will cascade delete dogs, comments, etc)
            user.delete()
            flash('Account deleted! Hope to see you again', 'check-circle')
            return redirect(url_for('main.index'))

    return render_template('user/delete_account.html', user=user,
                           title='Delete Account', form=form)


@users.route('/like/<dog_id>')
@login_required
def like(dog_id):
    """
    Route for liking a dog and increasing their
    like count
    """
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

    # Return to previous page ensuring no repeating animation if coming from
    # gallery view
    return redirect(
        request.referrer) if '/profile/' in request.referrer else deanimate(
        request.referrer)


@users.route('/favourite/<dog_id>')
@login_required
def favourite(dog_id):
    """
    Route for saving a dog to the current
    user's favourites
    """
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

    # Return to previous page ensuring no repeating animation if coming from
    # gallery view
    return redirect(
        request.referrer) if '/profile/' in request.referrer else deanimate(
        request.referrer)


@users.route('/edit_comment/<comment_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    form = CommentInput()
    comment = Comment.objects(pk=comment_id).first()
    if comment.author != current_user and current_user.username != 'admin':
        flash("You cannot edit someone else's comment!", "exclamation")
        return redirect(url_for('main.gallery', view='hot'))
    dog_id = comment.dog.pk
    if form.validate_on_submit():
        comment.content = form.content.data
        comment.save()
        flash("Comment edited", "comment")
        return redirect(url_for('dogs.dog_page', dog_id=dog_id))
    form.content.data = comment.content
    return render_template('user/edit_comment.html', form=form,
                           comment=comment, title="Edit Comment")


@users.route('/delete_comment/<comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.objects(pk=comment_id).first()
    if comment.author != current_user and current_user.username != 'admin':
        flash("You cannot delete someone else's comment!", "exclamation")
        return redirect(url_for('main.gallery', view='hot'))
    dog_id = comment.dog.pk
    if request.method == 'POST':
        comment.delete()
        flash("Comment deleted", "comment")
        return redirect(url_for('dogs.dog_page', dog_id=dog_id))
    return render_template('user/delete_comment.html', comment=comment,
                           title="Delete Comment")
