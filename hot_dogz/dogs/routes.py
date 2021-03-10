from hashlib import new
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login.utils import login_required
from hot_dogz.dogs.forms import CommentInput, UploadForm, EditForm
from flask_login import current_user
from hot_dogz.models import Comment, Dog, Breed

dogs = Blueprint('dogs', __name__)


@dogs.route('/upload_dog', methods = ['GET', 'POST'])
# Removed @login_required for this route
# as it was preventing flash message from working
def upload_dog():
    """
    Route for uploading a dog to the database
    """
    if current_user.is_anonymous:
        flash('You must be a registered user to do that!', 'exclamation')
        return redirect(url_for('users.login'))
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
    """Route for editing a dog's details"""
    dog = Dog.objects(pk=dog_id).first()
    form = EditForm()
    if form.validate_on_submit():
        # Update Breed and about section
        dog.update(name=form.name.data)
        new_breed = Breed.objects(pk=form.breed.data).first()
        dog.update(breed=new_breed)
        dog.update(about=form.about.data)
        # If an imgage is selected, run set image function on Dog model
        if(form.img_url.data):
            dog.set_dog_image(form.img_url.data, current_user.username, dog.pk)
        dog.save()
        flash('Updated dog details!', 'check-circle')
        return redirect(url_for('users.profile', username=current_user.username))
    # Pre-fill data for GET requests
    elif request.method == 'GET':
        form.name.data = dog.name
        form.breed.data = dog.breed.breed_name
        form.about.data = dog.about
    return render_template('upload_dog.html', form=form, title="Edit Dog")


@dogs.route('/delete_dog/<dog_id>', methods=['GET', 'POST'])
@login_required
def delete_dog(dog_id):
    """Route for deleting a dog from database"""
    dog = Dog.objects(pk=dog_id).first()
    if request.method == 'POST':
        user = current_user.username
        # Delete dog's image from cloudinary database before deleting dog
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