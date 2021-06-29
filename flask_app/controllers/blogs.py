from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models import team, user, blog

@app.route("/create_blog")
def create_blog():
    # blogs = blog.Blog.unassigned_users()
    return render_template("create_blog.html")

@app.route("/create_blog/save", methods = ["POST"])
def save_blog():
    if not blog.Blog.validate_blog(request.form):
        return redirect("/create_blog")
    
