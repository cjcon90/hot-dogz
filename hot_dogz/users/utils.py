from flask import render_template, current_app, redirect, url_for
from hot_dogz.main.utils import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Hot Dogz] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def deanimate(path):
    """
    function to ensure that user returns to correct
    page in gallery after liking favouriting
    but without repeating gallery page animation
    """
    view = 'new' if 'new?' in path else 'hot'
    # Parse the return URL for page number
    page = path.replace('&animate=False', '').split('page=')[
        -1] if 'page=' in path else '1'
    return redirect(
        url_for('main.gallery', view=view, page=page, animate=False))
