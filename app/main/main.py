import os

from flask import render_template, request
import datetime
import requests
from app.run import app
import smtplib
from dotenv import load_dotenv

load_dotenv()
blog_posts = requests.get("https://api.npoint.io/262dc4522e0bbf0e6be3").json()
day = datetime.date.today()


def send_email(name, email, phone, message):
    message = f"""Subject: New Message from {name}-{day.day}-{day.month}-{day.year}\n
    {message}. Have  Wonderful Day ahead!\n
    BR,
    {name}
    {email}
    {phone}
    """
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465) as connection:
        # secure the connection(packets sent using ttls)
        connection.ehlo()
        connection.login(user=os.getenv('user'), password=os.getenv('password'))
        connection.sendmail(
            from_addr=os.getenv('my_email'),
            to_addrs=os.getenv('my_email'),
            msg=message)


@app.route('/')
def get_posts_all():
    return render_template('index.html', posts=blog_posts, year=day.year)


@app.route('/about')
def about():
    return render_template('about.html', year=day.year)


@app.route('/show_post/<int:index>')
def show_post(index):
    requested_post = None
    for blog in blog_posts:
        if blog["id"] == index:
            requested_post = blog
    return render_template("post.html", post=requested_post, year=day.year)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(name=data['name'], email=data['email'], phone=data['phone'], message=data['message'])
        return render_template('contact.html', msg_sent=True, year=day.year)
    return render_template('contact.html', msg_sent=False, year=day.year)
