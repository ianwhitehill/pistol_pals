from flask_bcrypt import Bcrypt
from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models.user import User   
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
        "role_id": request.form["role_id"],
        "sight_id": request.form["sight_id"]

    }
    print(request.form)
    user_id = User.create_user(data)

    session["user_id"] = user_id
    session["first_name"] = request.form["first_name"]
    session["role_id"] = request.form["role_id"]

    if request.form["role_id"] == "2":
        users = User.unassigned_users()
        return render_template("create_team.html", users =  users)
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
    session["role_id"] = user_in_db.role_id
    session["last_name"] = user_in_db.last_name
    print("id in session")
    return redirect("/user/dashboard")

@app.route("/user/dashboard")
def user_homepage():
    if not "user_id" in session:
        return redirect("/")
    return render_template("standings.html")


@app.route("/user/logout")
def logout():
    session.clear()
    return redirect("/")