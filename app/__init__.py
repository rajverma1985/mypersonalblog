from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
password = quote_plus(f"{os.environ['DB_PASSWORD']}")
DB_URI = f"postgresql://{os.environ['DB_USER']}:{password}@{os.environ['DB_SERVER']}/{os.environ['DB']}"
engine = create_engine(DB_URI)
if not database_exists(engine.url):
    create_database(engine.url)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9BYkEfBA6O6donzWlSihBXox7C0sKR6c'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
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
