from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import logging

# Logging 
logging.basicConfig(filename='dd.log', level=logging.INFO, format='%(levelname)s:%(message)s')

# App Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cw@localhost/devlist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Developer Class/Model
class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    screenname = db.Column(db.String(50))
        
    def __init__(self, username, screenname):
        self.username = username
        self.screenname = screenname
        logging.info('Created Developer: {} - {}'.format(self.username, self.screenname))
        
# POST New Dev Info
@app.route('/devs', methods=['POST'])
def add_devs():
    username = request.json['username']
    screenname = request.json['screenname']
    new_dev = Developer(username, screenname)
    db.session.add(new_dev)
    db.session.commit()    
    return {"username": new_dev.username, "screenname": new_dev.screenname}

# GET All Devs Info
@app.route('/devs')
def get_devs():
    devs = Developer.query.all()
    output = []
    for dev in devs:
        dev_data = {'id': dev.id, 'username': dev.username, 'screenname': dev.screenname}
        output.append(dev_data)
    return {"devs": output}

# GET Specific Dev Info
@app.route('/devs/<id>')
def get_dev(id):
    dev = Developer.query.get_or_404(id)
    return {"username": dev.username, "screenname": dev.screenname}

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
