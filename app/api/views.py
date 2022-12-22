from datetime import date
from functools import wraps
from flask import render_template, redirect, url_for, abort
from flask_login import current_user
from app.api.forms import CreatePostForm
from app.models import BlogPost
from app import db
from app.api import api


def admin_only(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        """checking for anonymous user and admin user here"""
        if not current_user.is_authenticated or (current_user.is_authenticated and current_user.id != 1):
            return abort(403)
        return func(*args, **kwargs)

    return wrapper_func


@api.route('/')
def get_all_posts():
    blog_posts = BlogPost.query.all()
    return render_template("index.html", all_posts=blog_posts)


@api.route('/new-post', methods=['GET', 'POST'])
@admin_only
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        add_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            author=current_user,
            img_url=form.img_url.data,
            date=date.today().strftime("%B %d, %Y")
          )
        db.session.add(add_post)
        db.session.commit()
        return redirect(url_for('api.get_all_posts'))
    return render_template('make-post.html', form=form, current_user=current_user)


@api.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)


@api.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(title=post.title,
                               subtitle=post.subtitle,
                               img_url=post.img_url,
                               author=post.author,
                               body=post.body)
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("api.show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@api.route('/delete_post/<int:post_id>')
@admin_only
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@api.route("/about")
def about():
    return render_template("about.html")


@api.route("/contact")
def contact():
    return render_template("contact.html")
