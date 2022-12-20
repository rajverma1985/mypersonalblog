from flask import render_template, redirect, url_for
from app.auth import auth
from app.auth.forms import RegisterForm


@auth.route('/register')
def register():
    registration = RegisterForm()
    return render_template("register.html", form=registration)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return redirect(url_for('get_all_posts'))