from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models import team, user


@app.route("/create_team")
def create_team():
    users = user.User.unassigned_users()
    return render_template("create_team.html", users = users)

@app.route("/create_team/save", methods = ["POST"])
def save_team():
    # validate the team user input
    if not team.Team.validate_team(request.form):
        return redirect("/create_team")


    # pass through form data
    team_data = {
        "name": request.form["name"],
        "captain_id": request.form["captain_id"]
    }
    team_id = team.Team.create_team(team_data)
    print(team_id)

    # assign the members selected their team id
    member_1_data =  {
        "user_id": request.form["member_1"],
        "team_id": team_id
    }
    member_2_data = {
        "user_id": request.form["member_2"],
        "team_id": team_id
    }

    captain_data = {
        "user_id":request.form["captain_id"],
        "team_id": team_id
    }
    user.User.assign_team_id(member_1_data)
    user.User.assign_team_id(member_2_data)
    user.User.assign_team_id(captain_data)

    return redirect(f"/review/{team_id}")

@app.route("/review/<team_id>")
def review_team(team_id):
    # get team by id and display info by jinja on template
    return render_template("review_team.html")



