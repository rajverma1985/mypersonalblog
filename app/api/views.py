from datetime import date
from flask import render_template, redirect, url_for, Blueprint
from app.api.forms import CreatePostForm
from app.models import BlogPost
from app import db
from app.api import api


@api.route('/')
def get_all_posts():
    blog_posts = BlogPost.query.all()
    return render_template("index.html", all_posts=blog_posts)


@api.route('/new-post', methods=['GET', 'POST'])
def new_post():
    blog_form = CreatePostForm()
    today = date.today().strftime("%d %B %Y")
    if blog_form.validate_on_submit():
        add_post = BlogPost(title=blog_form.title.data, date=today, subtitle=blog_form.subtitle.data,
                            body=blog_form.body.data,
                            author=blog_form.author.data, img_url=blog_form.img_url.data)
        db.session.add(add_post)
        db.session.commit()
        return redirect(url_for('new_post'))
    return render_template('make-post.html', form=blog_form)


@api.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)


@api.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
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
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@api.route('/delete_post/<int:post_id>')
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
