from flask import Blueprint
from flask_restful import Api
from resources.User import User
from resources.Task import Task

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(User, '/User')
api.add_resource(Task, '/Task')