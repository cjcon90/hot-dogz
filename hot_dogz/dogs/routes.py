from hashlib import new
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login.utils import login_required
from hot_dogz.dogs.forms import CommentInput, UploadForm, EditForm
from flask_login import current_user
from hot_dogz.models import Comment, Dog, Breed

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


@dogs.route('/edit_dog/<dog_id>', methods=['GET', 'POST'])
@login_required
def edit_dog(dog_id):
    dog = Dog.objects(pk=dog_id).first()
    form = EditForm()
    if form.validate_on_submit():
        dog.update(name=form.name.data)
        new_breed = Breed.objects(pk=form.breed.data).first()
        dog.update(breed=new_breed)
        dog.update(about=form.about.data)
        if(form.img_url.data):
            dog.set_dog_image(form.img_url.data, current_user.username, dog.pk)
        dog.save()
        flash('Updated dog details!', 'check-circle')
        return redirect(url_for('users.profile', username=current_user.username))
    elif request.method == 'GET':
        form.name.data = dog.name
        form.breed.data = dog.breed.breed_name
        form.img_url.data = dog.img_url
        form.about.data = dog.about
    return render_template('upload_dog.html', form=form, title="Edit Dog")


@dogs.route('/delete_dog/<dog_id>', methods=['GET', 'POST'])
@login_required
def delete_dog(dog_id):
    dog = Dog.objects(pk=dog_id).first()
    if request.method == 'POST':
        user = current_user.username
        dog.delete_dog_image(user, dog.pk)
        dog.delete()
        flash("Dog post successfuly deleted", "check-circle")
        return redirect(url_for('users.profile', username=user))
    return render_template('delete_dog.html', dog=dog)


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