#code for your application

from flask_restful import Resource

class User(Resource):
    def get(self):
        return {"message": "The Usoooor!"}