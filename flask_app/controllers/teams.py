from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models import team, user


@app.route("/create_team")
def create_team():
    users = user.User.unassigned_users()
    return render_template("create_team.html", users = users)

@app.route("/create_team/save", methods = ["POST"])
def save_team():
    if not team.Team.validate_team(request.form):
        return redirect("/create_team")
    


