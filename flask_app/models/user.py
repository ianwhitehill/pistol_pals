from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re

class User: 
    def __init__(self, data): 
        self.id = data["id"]
        self.username = data["username"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.team_id = data["team_id"]
        self.role = data["role"]
        self.sight = data["sight"]
        self.total_score = 0


    @classmethod
    def unassigned_users(cls):
        query = "SELECT * FROM users WHERE users.role = 3 AND users.team_id IS null;"
        results = connectToMySQL("pp").query_db(query)
        unassigned_users = []
        for user in results: 
            unassigned_users.append(cls(user))
        return unassigned_users

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (username, first_name, last_name, email, password, created_at, updated_at, role, sight) VALUES (%(username)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW(), %(role)s, %(sight)s);"
        return connectToMySQL("pp").query_db(query, data)


    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL("pp").query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls,data):
        query ="SELECT * FROM users WHERE users.id = %(user_id)s;"
        result = connectToMySQL("pp").query_db(query,data)
        print(result)
        return cls(result[0])

    @classmethod
    def get_user_by_username(cls, data):
        query = "SELECT * FROM users WHERE users.username = %(username)s;"
        results = connectToMySQL("pp").query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_reg(data):
        is_valid = True
        
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


        if len(data["first_name"]) <= 2 or not data["first_name"].isalpha(): 
            flash("You last name must be longer than 2 characters.")
            is_valid = False
        
        if len(data["last_name"]) <= 2 or not data["last_name"].isalpha():
            flash("You last name must be longer than 2 characters of the English alphabet.")
            is_valid = False

        if not email_regex.match(data["email"]):  
            flash("Please enter a valid email.")
            is_valid = False

        if User.get_user_by_email(data): 
            flash("Email address already exsits!")
            is_valid = False
        
        if User.get_user_by_username(data):
            flash("Username is taken!")
            is_valid = False

        if len(data["password"]) < 8:
            flash("Password must be 8 or more characters")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("passwords must match")
            is_valid = False

        return is_valid

    @classmethod
    def assign_team_id(cls, data):
        query  = "UPDATE users SET team_id = %(team_id)s WHERE users.id IN (%(captain_id)s, %(member_1_id)s, %(member_2_id)s);"
        return connectToMySQL("pp").query_db(query, data)        