from werkzeug import datastructures
from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models import team, user, blog
from flask_app.models.blog import Blog

@app.route("/create_blog")
def create_blog():

    return render_template("create_blog.html")

@app.route("/create_blog/save", methods = ["POST"])
def save_blog():
    if  blog.Blog.validate_blog(request.form):
        data = {
            'title': request.form['blog_title'],
            'body': request.form['blog_body'],
            'author_id': session['user_id']
        }
        blog.Blog.create_blog(data)
        return redirect("/create_blog")

@app.route("/view_blog")
def view_blog():

    blogs = Blog.get_blog_by_id()
    print(blogs)

    return render_template("view_blog.html", blogs = blogs)
