from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models import team, user, blog

@app.route("/create_blog")
def create_blog():

    return render_template("create_blog.html")

@app.route("/create_blog/save", methods = ["POST"])
def save_blog():
    if  blog.Blog.validate_blog(request.form):
        data = {
            'blog_title': request.form['blog_title'],
            'blog_body': request.form['blog_body']
        }
        blog.Blog.create_blog(data)
        return redirect("/create_blog")

    
