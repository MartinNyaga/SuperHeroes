#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def home():
    response_body = {
        "Message": "Heroes, powers, strengths and weakness"
    }
    return make_response(jsonify(response_body), 200)

class Heroes(Resource):

    def get(self):

        heroes = Hero.query.all()
        heroes_list=[]
        for hero in heroes:
            heroes_dict = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
            }
            heroes_list.append(heroes_dict)
        response = make_response(jsonify(heroes_list), 200)
        return response
    

api.add_resource(Heroes, '/heroes')

class HeroesByID(Resource):

    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if not hero:
            return {"error": "Hero not found"}, 404
        
        response_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
        }
        return response_dict, 200
    
api.add_resource(HeroesByID, '/heroes/<int:id>')

class Powers(Resource):

    def get(self):

        powers = Power.query.all()
        powers_list=[]
        for power in powers:
            powers_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            }
            powers_list.append(powers_dict)
        response = make_response(jsonify(powers_list), 200)
        return response
    

api.add_resource(Powers, '/powers')

class PowersByID(Resource):

    def get(self, id):
        power = Power.query.filter_by(id=id).first()
        if not power:
            return {"error": "Power not found"}, 404
        
        response_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
        }
        return response_dict, 200
    
    def patch(self, id):
        power = Power.query.filter(Power.id == id).first()
        if not power:
            return {"error": "Power not found"}, 404

        for attr in request.form:
            if attr == 'description':
                setattr(power, attr, request.form.get(attr))

        db.session.commit()

        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
        }

        return make_response(jsonify(power_dict), 200)

    
api.add_resource(PowersByID, '/powers/<int:id>')

class HeroPower(Resource):
    
    def post(self):
        data = request.get_json()
        
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')
        
        new_hero_power = HeroPower()
        new_hero_power.strength = strength
        new_hero_power.power_id = power_id
        new_hero_power.hero_id = hero_id
        
        db.session.add(new_hero_power)
        db.session.commit()
        
        if new_hero_power.id:
            return make_response(jsonify(new_hero_power.to_dict()), 201)
        else:
            return make_response(jsonify({"errors": ["validation errors"]}), 404)

api.add_resource(HeroPower, '/heropowers')



if __name__ == '__main__':
    app.run(port=5555)
