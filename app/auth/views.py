from flask import render_template, redirect, url_for, flash, request
from app.auth import auth
from app.auth.forms import RegisterForm, LoginForm
from app.models import Users
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
        user = Users(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("api.get_all_posts"))
    return render_template("register.html", form=form)


@auth.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@auth.route('/logout')
def logout():
    return redirect(url_for('get_all_posts'))
