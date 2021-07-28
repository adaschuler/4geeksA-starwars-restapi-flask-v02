"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favoritespeople, Favoritesplanet, Favoritesvehicles, People, Planet, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    query_people = People.query.all()
    query_people = list(map(lambda x: x.serialize(), query_people))
    print(query_people)
    response_body = {
        "msg": "Hello, this is your GET /people response ",
        "people": query_people
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['POST'])
def post_people():
    body = request.get_json()
    print(body)
    people = People(name=body['name'])
    planet = Planet(name=body['planet'])
    db.session.add(people)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your POST /people response "
    }

    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    query_planet = Planet.query.all()
    query_planet = list(map(lambda x: x.serialize(), query_planet))
    print(query_planet)
    response_body = {
        "msg": "Hello, this is your GET /planet response ",
        "planet": query_planet
    }

    return jsonify(response_body), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():

    response_body = {
        "msg": "Hello, this is your GET /vehicles response "
    }

    return jsonify(response_body), 200    

# @app.route('/favoritespeople', methods=['GET'])
# def handle_favoritespeople():
#     query_favoritespeople = Favoritespeople.query.all()
#     query_favoritespeople = list(map(lambda x: x.serialize(), query_favoritespeople))
#     print(query_favoritespeople)
#     response_body = {
#         "msg": "Hello, this is your GET /favoritespeople response ",
#         "favoritespeople": query_favoritespeople
#     } 

#     return jsonify(response_body), 200

# if __name__ == '__main__':
#     PORT = int(os.environ.get('PORT', 3000))
#     app.run(host='0.0.0.0', port=PORT, debug=False)


# @app.route('/favoritespeople', methods=['POST'])
# def post_favoritespeople():
#     body = request.get_json()
#     print(body)
#     people = People(name=body['people'])
#     user = User(name=body['favorites'])
#     db.session.add(favoritespeople)
#     db.session.commit()
#     response_body = {
#         "msg": "Hello, this is your POST /favoritespeople response "
#     }

#     return jsonify(response_body), 200

@app.route('/user', methods=['GET'])
def handle_hello():
    query_user = User.query.all()
    query_user = list(map(lambda x: x.serialize(), query_user))
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "users":query_user
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
