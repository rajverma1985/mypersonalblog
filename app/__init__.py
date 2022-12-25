from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9BYkEfBA6O6donzWlSihBXox7C0sKR6c'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True

    Bootstrap(app)
    # Initialize DB
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    ckeditor.init_app(app)
    register_bp(app)
    with app.app_context():
        db.create_all()
    return app


# register blueprints
def register_bp(app):
    from app.api.views import api
    from app.auth.views import auth
    app.register_blueprint(api)
    app.register_blueprint(auth, url_prefix='/auth')

# todo: add logger, add extensions, filters, error handler, db customization
