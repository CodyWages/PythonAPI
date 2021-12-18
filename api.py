from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from requests import get

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
api = Api(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    screenname = db.Column(db.String(50))

    def __init__(self, id, username, screenname):
        self.id = id
        self.username = username
        self.screenname = screenname
        
    def __repr__(self):
        return f"{self.username} - {self.screenname}"

@app.route('/devs')
def get_devs():
    devs = User.query.all()
    output = []
    
    for dev in devs:
        dev_data = {'username': dev.name, 'screenname': dev.screenname}
        output.append(dev_data)
    return {"devs": output}

@app.route('/devs/<id>')
def get_dev(id):
    dev = User.query.get_or_404(id)
    return {"name": dev.username, "description": dev.screenname}

if __name__ == '__main__':
    app.run(debug=True)