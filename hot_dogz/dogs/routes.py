from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login.utils import login_required
from hot_dogz.dogs.forms import CommentInput, UploadForm
from flask_login import current_user
from hot_dogz.models import Comment, Dog

dogs = Blueprint('dogs', __name__)

@dogs.route('/upload_dog', methods = ['GET', 'POST'])
@login_required
def upload_dog():
    """
    Route for uploading a dog to the database
    """
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Upload dog and add owner to likes by default
        dog = Dog(name=form.name.data, owner=current_user.id, breed=form.breed.data,about=form.about.data, liked_by=[current_user.id], likes=1)
        dog.save()
        # Set dog image url to be dog's primary key, for easy deletion and overwriting
        dog.set_dog_image(form.img_url.data, current_user.username, dog.pk)
        dog.save()
        flash('Dog Uploaded!', 'dog')
        return redirect(url_for('users.profile', username=current_user.username))
    # 'GET' functioning
    return render_template('upload_dog.html', form=form, title="Upload Dog")


@dogs.route('/dog/<dog_id>', methods=['GET', 'POST'])
def dog_page(dog_id):
    """
    Route for displaying the a dog's profile page,
    with larger image, about info and comment section
    """
    dog = Dog.objects(pk=dog_id).first()
    form = CommentInput()
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(author=current_user.id, dog=dog, content=form.content.data)
        comment.save()
        flash('Your comment has been submitted!', 'comment')
        return redirect(url_for('dogs.dog_page', dog_id=dog_id))
    comments=Comment.objects(dog=dog)
    for comment in comments:
        print(comment)
    return render_template('dog_page.html', dog=dog, form=form, comments=comments, title=f"{dog.name}'s Page")