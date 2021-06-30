
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

    # this method returns a list of the members who are not captain.
    @classmethod
    def members_no_capt(cls, data):
        query = "SELECT * FROM users JOIN teams ON teams.id = users.team_id WHERE teams.id = %(team_id)s;"
        results = connectToMySQL("pp").query_db(query, data)
        sorted_members = []
        for member in results:
            if member["role"] == 3:
                sorted_members.append(member)
        return sorted_members

    #returns just the captain and their team information.  
    @classmethod
    def get_captain(cls, data):
        query = "SELECT * FROM users JOIN teams ON users.id = teams.captain_id WHERE users.id = %(captain_id)s;"
        result = connectToMySQL("pp").query_db(query,data)
        return result[0]

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
            # get a list of team members 
            team.members.append(user.User(user_data))

        return team    

    @classmethod
    def update_team(cls, data1, data2, data3):
        # update team name
        query = "UPDATE teams SET name = %(name)s WHERE teams.id = %(team_id)s;"
        connectToMySQL("pp").query_db(query,data1)

        # delete team id from previous
        query = "UPDATE users SET team_id = null WHERE users.id IN (%(old_member_1)s,%(old_member_2)s);" 
        connectToMySQL("pp").query_db(query,data3)   

        # reassign team id to new // if the user_id remains the same it will reassign same team_id
        query = "UPDATE users SET team_id = %(team_id)s WHERE users.id IN (%(member_1)s, %(member_2)s);"
        connectToMySQL("pp").query_db(query,data2)