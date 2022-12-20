from flask import render_template, redirect, url_for, flash, request
from app.auth import auth
from app.auth.forms import RegisterForm, LoginForm
from app.models import Users
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from app import login_manager


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if Users.query.filter_by(email=form.email.data).first():
            # flash messsage
            flash("You've already signed up with that email, Please log in instead!")
            # Redirect to /login route.
            return redirect(url_for('auth.login'))
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
        user = Users(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("api.get_all_posts"))
    return render_template("register.html", form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('auth.login'))
        elif not check_password_hash(user.password, password):
            flash("Incorrect Password!, please try again.")
            return redirect(url_for('auth.login'))
        else:
            login_user(user)
            return redirect(url_for('api.get_all_posts'))
    return render_template("login.html", form=form)


@auth.route('/logout')
def logout():
    return redirect(url_for('get_all_posts'))
