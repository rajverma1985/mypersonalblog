from flask import render_template
import requests
from app.run import app

blog_posts = requests.get("https://api.npoint.io/26e3f14416accc8b8c9b")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/sample_post')
def sample_post():
    return render_template('post.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')
