from flask_app.config.mysqlconnection import connectToMySQL
from flask import request
from flask import flash

class Blog:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.post = data["post"]
        self.author.id = data["author.id"]

    @classmethod
    def create_blog(cls, data):
        query = "INSERT INTO teams (name, captain_id) VALUES (%(name)s, %(captain_id)s);"
        return connectToMySQL("pistol_pals_personal").query_db(query, data)


    @staticmethod
    def validate_blog(data):
        is_valid =  True

        if data["blog_title"] == "":
            flash("Title cannot be blank")
            is_valid = False

        if data["blog_body"] == "":
            flash("Body cannot be blank")
            is_valid = False

        return is_valid