#code for your application

from flask_restful import Resource

class Task(Resource):
    def get(self):
        return {"message": "Agghhhh I'm gonna Task!"}