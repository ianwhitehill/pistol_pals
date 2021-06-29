
from flask_app.config.mysqlconnection import connectToMySQL
from flask import request
from flask import flash
from flask_app.models import user

class Team:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.captain_id = data["captain_id"]
        self.members = []


    @classmethod
    def validate_team(cls, data):
        is_valid =  True

        if data["member_1"] == data["member_2"]:
            flash("Cannot select the same member.")
            is_valid = False

        if len(data["name"]) < 2:
            flash("Team name must be longer than 2 characters.")
            is_valid = False

        return is_valid

    @classmethod
    def create_team(cls, data):
        query = "INSERT INTO teams (name, captain_id) VALUES (%(name)s, %(captain_id)s);"
        return connectToMySQL("pp").query_db(query, data)
    
    @classmethod
    def view_team_by_id(cls, data):
        query = "SELECT * FROM teams JOIN users ON users.team_id = teams.id WHERE teams.id = %(team_id)s;"
        results = connectToMySQL("pp").query_db(query, data)
        team = cls(results[0])


        for row in results:
            user_data = {
                "id": row["users.id"],
                'username':row["username"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "team_id": row["team_id"],
                "role": row["role"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "sight": row["sight"],
                "total_score": row["total_score"]
            }
            team.members.append(user.User(user_data))

        return team     