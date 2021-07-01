from flask.globals import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Event():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.start_time = data['start_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def select_all(cls):
        query = "SELECT * FROM events;"
        connection = connectToMySQL('pp')
        results = connection.query_db(query)
        events = []
        for result in results:
            event = Event(result)
            events.append(event)
        return events

    @classmethod
    def insert(cls, data):
        query  = "INSERT INTO events (name, descriton, start_time) VALUES (%(name)s, %(description)s, %(start_time)s);"
        connection = connectToMySQL('pp')
        results = connection.query_db(query, data)
        return results

    @classmethod
    def select_by_id(cls, data):
        query = "SELECT * FROM events WHERE id= %(id)s;"
        connection = connectToMySQL('pp')
        result = connection.query_db(query, data)
        return result

    @classmethod
    def update(cls, data):
        query = "UDPATE events SET name = %(name)s, description = %(description)s, start_time = %(start_time)s;"
        connection = connectToMySQL('pp')
        connection.query_db(query, data)

    @classmethod
    def remove(cls, data):
        query = "DELETE FROM events WHERE id = %(id)s;"'
        connection = connectToMySQL('pp')
        connection.query_db(query, data)

    @staticmethod
    def validation(data):
        is_valid = True 

        if len(data['name']) < 2 or len(data['name']) > 45:
            is_valid = False
            flash('Name must be greater then 2 or less the 45 characters')

        if data['start_time'] == None:
            is_valid = False
            flash('must input a start date  and time for the event')

        return is_valid