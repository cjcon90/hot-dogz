from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login.utils import login_required
from hot_dogz.dogs.forms import CommentInput, UploadForm
from flask_login import current_user
from hot_dogz.models import Comment, Dog

dogs = Blueprint('dogs', __name__)

@dogs.route('/upload_dog', methods = ['GET', 'POST'])
@login_required
def upload_dog():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        dog = Dog(name=form.name.data, owner=current_user.id, breed=form.breed.data,about=form.about.data)
        dog.set_dog_image(form.img_url.data, current_user.username)
        dog.save()
        flash('Dog Uploaded!')
        return redirect(url_for('users.profile', username=current_user.username))
    # 'GET' functioning
    return render_template('upload_dog.html', form=form, title="Upload Dog")


@dogs.route('/dog/<dog_id>', methods=['GET', 'POST'])
def dog_page(dog_id):
    dog = Dog.objects(pk=dog_id).first()
    form = CommentInput()
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(author=current_user.id, dog=dog, content=form.content.data)
        comment.save()
        flash('Your comment has been submitted!')
        return redirect(url_for('dogs.dog_page', dog_id=dog_id))
    comments=Comment.objects(dog=dog)
    for comment in comments:
        print(comment)
    return render_template('dog_page.html', dog=dog, form=form, comments=comments)