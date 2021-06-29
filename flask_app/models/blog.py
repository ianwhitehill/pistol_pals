
from flask import request
from flask import flash

class Blog:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.post = data["post"]
        self.author.id = data["author.id"]


    @classmethod
    def validate_blog(cls, data):
        is_valid =  True

        if data["blog_title"] == "":
            flash("Cannot select the same member.")
            is_valid = False

        # if len(data["team_name"]) < 2:
        #     flash("Team name must be longer than 2 characters.")
        #     is_valid = False

        return is_valid