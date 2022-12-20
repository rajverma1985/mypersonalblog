from flask import Flask, render_template, json
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
import os

db = SQLAlchemy()
ckeditor = CKEditor()
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9BYkEfBA6O6donzWlSihBXox7C0sKR6c'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Bootstrap(app)
    # CONNECT TO DB

    db.init_app(app)
    ckeditor.init_app(app)
    register_bp(app)
    # db.create_all()
    return app


# register blueprints
def register_bp(app):
    from app.api.views import api
    app.register_blueprint(api)
