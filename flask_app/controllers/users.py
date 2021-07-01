from flask_bcrypt import Bcrypt
from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models.user import User
from flask_app.models import team  
bcrypt = Bcrypt(app) 


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/user/register")
def register():
    return render_template("register.html")

@app.route("/user/register/save", methods=["POST"])
def register_user():
    print("validating")
    # validate users info 
    if not User.validate_reg(request.form):
        print("not valid")
        return redirect("/user/register")
    #hash the password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "username": request.form["username"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password" : pw_hash,
        "role": request.form["role"],
        "sight": request.form["sight"]

    }
    print(request.form)
    user_id = User.create_user(data)
    session["user_id"] = user_id

    if request.form["role"] == "2":
        users = User.unassigned_users()
        return render_template("teams/create_team.html", users =  users)
    else: 
        return render_template("standings.html")

@app.route("/user/login", methods=['POST'])
def login_user():
    print(request.form)
    print("loggin_in")
    # create data to get the user by email in database
    data = {
        "email": request.form["email"]}
    # if theyre not the database prompt them to register
    user_in_db = User.get_user_by_email(data)
    print(user_in_db)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    #if their password doesnt match prompt them to try again
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    # else put their id into session 
    session["user_id"] = user_in_db.id
    session["first_name"] = user_in_db.first_name
    session["role"] = user_in_db.role
    session["last_name"] = user_in_db.last_name
    print("id in session")
    return redirect("/user/dashboard")

@app.route("/user/dashboard")
def user_homepage():
    if not "user_id" in session:
        return redirect("/")
    data = {
        "user_id": session["user_id"]
    }
    user = User.get_user_by_id(data)
    teams = team.Team.all_teams()
    iron = User.get_iron()
    laser = User.get_laser()
    red_dot = User.get_red_dot()


    return render_template("standings.html", user = user, teams = teams, iron = iron, red_dot = red_dot, laser = laser)


@app.route("/user/logout")
def logout():
    session.clear()
    return redirect("/")