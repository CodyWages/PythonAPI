from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cw@localhost/devlist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    screenname = db.Column(db.String(50))
        
    def __init__(self, username, screenname):
        self.username = username
        self.screenname = screenname

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'screenname')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/devs', methods=['POST'])
def add_devs():
    username = request.json['username']
    screenname = request.json['screenname']
    new_dev = User(username, screenname)
    db.session.add(new_dev)
    db.session.commit()
    return user_schema.jsonify(new_dev)

@app.route('/devs')
def get_devs():
    devs = User.query.all()

    output = []
    for dev in devs:
        dev_data = {'username': dev.username, 'screenname': dev.screenname}
        output.append(dev_data)
    return {"devs": output}

@app.route('/devs/<id>')
def get_dev(id):
    dev = User.query.get_or_404(id)
    return {"name": dev.username, "description": dev.screenname}

if __name__ == '__main__':
    app.run(debug=True)