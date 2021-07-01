from flask_app.config.mysqlconnection import connectToMySQL
from flask import request
from flask import flash
from flask_app.models.user import User

class Blog:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.body = data["body"]
        self.author.id = data["author.id"]
        self.creator = None

    @classmethod
    def create_blog(cls, data):
        query = "INSERT INTO blog (title, body, author_id) VALUES (%(title)s, %(body)s, %(author_id)s);"
        return connectToMySQL("pp").query_db(query, data)

    @classmethod
    def get_blog_by_id(cls):
        query = 'SELECT * FROM blog ORDER BY created_at DESC;'

        connection = connectToMySQL('pp')
        results = connection.query_db(query)

        return results


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