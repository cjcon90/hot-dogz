from app import app, db
from app.models import User

# automatically add database instance and models to 'flask shell'
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}