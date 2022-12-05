from flask import render_template, request, jsonify
import requests
from app.run import app

blog_posts = requests.get("https://api.npoint.io/26e3f14416accc8b8c9b").json()


@app.route('/')
def get_posts_all():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/show_post/<int:id>')
def show_post(index):
    requested_post = None
    for blog in blog_posts:
        if blog["id"] == index:
            requested_post = blog
    return render_template("post.html", post=requested_post)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        data = request.data
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)
