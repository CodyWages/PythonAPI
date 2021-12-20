from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Init App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cw@localhost/devlist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

#User Class/Model
class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    screenname = db.Column(db.String(50))
        
    def __init__(self, username, screenname):
        self.username = username
        self.screenname = screenname

#User Schema
class DeveloperSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'screenname')
dev_schema = DeveloperSchema()
devs_schema = DeveloperSchema(many=True)

#POST new dev info
@app.route('/devs', methods=['POST'])
def add_devs():
    username = request.json['username']
    screenname = request.json['screenname']
    new_dev = Developer(username, screenname)
    db.session.add(new_dev)
    db.session.commit()
    return dev_schema.jsonify(new_dev)

#GET all devs info
@app.route('/devs')
def get_devs():
    devs = Developer.query.all()

    output = []
    for dev in devs:
        dev_data = {'id': dev.id, 'username': dev.username, 'screenname': dev.screenname}
        output.append(dev_data)
    return {"devs": output}

#GET specific dev info
@app.route('/devs/<id>')
def get_dev(id):
    dev = Developer.query.get_or_404(id)
    return {"name": dev.username, "description": dev.screenname}

#Run Server
if __name__ == '__main__':
    app.run(debug=True)