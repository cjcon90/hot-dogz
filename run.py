from hot_dogz import create_app, db
from hot_dogz.models import Comment, User, Dog, Breed

app = create_app()


# automatically add database instance and models to flask shell for use in debugging
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Dog': Dog, 'Breed': Breed, 'Comment': Comment}
