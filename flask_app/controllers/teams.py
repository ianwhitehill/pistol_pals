from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models import team, user


@app.route("/create_team")
def create_team():
    users = user.User.unassigned_users()
    return render_template("teams/create_team.html", users = users)

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
    data =  {
        "member_1_id": request.form["member_1"],
        "team_id": team_id,
        "member_2_id": request.form["member_2"],
        "captain_id": session["user_id"]
    }
    user.User.assign_team_id(data)

    return redirect(f"/review/{team_id}")

@app.route("/review/<int:team_id>")
def review_team(team_id):
    # get team information -
    team_id_data = {
        "team_id": team_id
    }
    team_in_db = team.Team.view_team_by_id(team_id_data)

    # get captain 
    captain_id_data = {
        "captain_id": team_in_db.captain_id }
    captain = team.Team.get_captain(captain_id_data)

    # get regular members  captain 
    members = team.Team.members_no_capt(team_id_data)
    return render_template("teams/review_team.html", team = team_in_db, captain = captain, members = members)

@app.route("/edit/<int:team_id>")
def edit_team(team_id):
    data = {
        "team_id": team_id
    }
    team_in_db = team.Team.view_team_by_id(data)
    unassigned_users = user.User.unassigned_users()
    members = team.Team.members_no_capt(data)
    return render_template("teams/edit_team.html", team = team_in_db, unassigned_users = unassigned_users, members = members)

@app.route("/update/<int:team_id>", methods = ["POST"])
def update_team(team_id):
    data = {
        "member_1": request.form["member_1"],
        "member_2": request.form["member_2"],
        "name": request.form["name"]

    }
    if not team.Team.validate_team(data):
        return redirect(f"/edit/{team_id}")
    # create data to pass to the query
    data1 = {
        "team_id": team_id,
        "name": request.form["name"]
    }
    data2 = {
        "team_id": team_id,
        "member_1": request.form["member_1"],
        "member_2": request.form["member_2"]
    }
    data3 = {
        "old_member_1": request.form["old_member_1"],
        "old_member_2": request.form["old_member_2"],
    }

    team.Team.update_team(data1, data2, data3)
    return redirect(f"/review/{team_id}")

@app.route("/myteam/<team_id>")
def my_team(team_id):
    # get team info
    team_data = {
        "team_id": team_id
    }
    team_in_db = team.Team.view_team_by_id(team_data)

    # get captain information
    data = {
        "captain_id": team_in_db.captain_id
    }
    captain = team.Team.get_captain(data)
    return render_template("teams/my_team.html", team = team_in_db, captain = captain)

