from flask import render_template
from app.run import app


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
