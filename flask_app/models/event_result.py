from flask.globals import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.event import Event


class Event_Results():
    def __init__(self, data):
        self.id = data['id']
        self.score = data['score']
        self.target_img1 = data['target_img1']
        self.target_img2 = data['target_img2']
        self.target_img3 = data['target_img3']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.event = None
        self.team = None

    @classmethod
    def select_all(cls):
        query = "SELECT * FROM event_results JOIN users ON user_id = users.id JOIN events ON event_id = events.id JOIN teams ON team_id = team.id;"
        connnection = connectToMySQL('pp')
        results = connnection.query_db(query)
        event_results = []
        for result in results:
            event_results = Event_Results(results)
            event_data = {
                'id' : result['event.id'],
                'name' : result['name'],
                'description' : result['description'],
                'start_time' : result['start_time'],
                'created_at' : result['event.created_at'],
                'updated_at' : results['event.updated_at']
            }
            event_results.event = Event(event_data)
            user_data = {}
            event_results.user = Event(user_data)
            team_data = {}
            event_results.team = Event(team_data)
            return event_results
    @classmethod
    def select_by_id(cls, data):
        query = "SELECT * FROM event_results JOIN users ON user_id = users.id JOIN events ON event_id = events.id JOIN teams ON team_id = team.id WHERE id = %(id)s;"
        connnection = connectToMySQL('pp')
        results = connnection.query_db(query)
        event_results = []
        for result in results:
            event_results = Event_Results(results)
            event_data = {
                'id' : result['event.id'],
                'name' : result['name'],
                'description' : result['description'],
                'start_time' : result['start_time'],
                'created_at' : result['event.created_at'],
                'updated_at' : results['event.updated_at']
            }
            event_results.event = Event(event_data)
            user_data = {}
            event_results.user = Event(user_data)
            team_data = {}
            event_results.team = Event(team_data)
            return event_results

        @classmethod
        def insert(cls, data):
            query = "INSERT INTO event_results (score, target_img1, target_img2, target_img3, user_id, event_id, team_id) VALUES (%(score)s, %(target_img1)s, %(target_img2)s, %(target_img3)s, %(user_id)s, %(event_id)s, %(team_id)s)"

            connection = connectToMySQL('pp')
            connection.query_db(query, data)

        @classmethod
        def update(cls, data):
            query = "UPDATE event_results SET score = %(score)s, target_img1 = %(target_img1)s, targat_img2 = %(target_img2)s, target_img3 = %(target_img3)s, user_id = %(user_id)s, event_id = %(event_id)s, team_id = %(team_id)s;"
            connection = connectToMySQL('pp')
            connection.query_db(query, data)

        @classmethod
        def delete(cls, data):
            query = "DELETE FROM event_results WHERE id %(id)s"
            connection = connectToMySQL('pp')
            connection.query_db(query, data)