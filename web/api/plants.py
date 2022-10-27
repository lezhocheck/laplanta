from flask import Blueprint, request
from .auth import confirmation_required, Database
from .models import Plant
from bson.objectid import ObjectId


plants = Blueprint('plants', __name__)


@plants.route('/plant', methods=['POST'])
@confirmation_required
def add_plant(user_id: ObjectId):
    plant = Plant.from_input_form(request.json)
    db = Database()
    id = db.insert_plant(plant, user_id)
    return {'plant_id': str(id)}


@plants.route('/plants')
@confirmation_required
def get_plants(user_id: ObjectId):
    db = Database()
    plants = db.get_plants(user_id)
    plants_obj = list(map(lambda x: x.to_dict_with_id(), plants))
    return {'plants': plants_obj}


@plants.route('/plant/<identifier>')
@confirmation_required
def get_plant(_, identifier: str):
    db = Database()
    plant = db.get_plant_by_id(ObjectId(identifier))
    return {'plant': plant.to_dict_with_id()} 


@plants.route('/plant/<identifier>', methods=['PUT'])
@confirmation_required
def update_plant(user_id: ObjectId, identifier: str):
    plant = Plant.from_update_form(request.json)
    plant.id = ObjectId(identifier)
    db = Database()
    db.update_plant(plant, user_id)


@plants.route('/plant/<identifier>', methods=['DELETE'])
@confirmation_required
def delete_plant(user_id: ObjectId, identifier: str):
    plant = Plant({'status': 'deleted'})
    plant.id = ObjectId(identifier)
    db = Database()
    db.update_plant(plant, user_id)