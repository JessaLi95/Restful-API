# Set up flask
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


# create a module for the database, and the sqlalchemy will inherit from (db.Model)
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


# Set up an endpoint/ a route
@app.route('/')
def index():
    return 'Hello!'


# export FLASK_APP=application.py
# export FLASK_ENV=development
# input the above command every time open the terminal
# flask run
# get an url


# create file name for the url
@app.route('/drinks')
def get_drinks():
    """get all the data in database"""
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)
    return {"drinks": output}


# create /drinks/id
@app.route('/drinks/<id>')
def get_drink(id):
    """get a data according to its id"""
    drink = Drink.query.get_or_404(id)
    return jsonify({"name": drink.name, "description": drink.description})  # use jsonify if not returning dict,
    # remember to 'from flask import jsonify


# POST
@app.route('/drinks', methods=['POST'])
def add_drink():
    """add a data"""
    drink = Drink(name=request.json['name'],
                  description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}


# DELETE
@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    """Delete an existed data"""
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "Not found"}
    else:
        db.session.delete(drink)
        db.session.commit()
        return {"message": "Deleted"}


# PUT
@app.route('/drinks/<id>', methods=['PUT'])
def update_drink(id):
    """Update an existed data"""
    data_to_update = Drink.query.get(id)
    if data_to_update is None:
        return {"error": "id not found, please create one."}
    else:
        data_to_update.name = request.json['name']
        data_to_update.description = request.json['description']
        db.session.commit()
        return jsonify({"message": "Data replaced"})