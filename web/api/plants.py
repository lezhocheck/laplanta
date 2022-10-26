from flask import Blueprint, request
from .auth import confirmation_required, Database
from .models import Plant
from .utils import DbError
from bson.objectid import ObjectId
from bson.errors import InvalidId


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
    def process(plant):
        result = plant.to_dict_row()
        result['id'] = str(plant.id)
        return result
    plants_obj = list(map(process, plants))
    return {'plants': plants_obj}


@plants.route('/plant/<identifier>')
@confirmation_required
def get_plant(user_id: ObjectId, identifier: str):
    try:
        db = Database()
        plant = db.get_plant_by_id(ObjectId(identifier))
        def process(plant):
            result = plant.to_dict_row()
            result['id'] = str(plant.id)
            return result
        return {'plant': process(plant)}
    except (InvalidId, TypeError):
        raise DbError('Invalid plant id')     


@plants.route('/plant/<identifier>', methods=['PUT'])
@confirmation_required
def update_plant(user_id: ObjectId, identifier: str):
    try:
        plant = Plant.from_update_form(request.json)
        plant.id = ObjectId(identifier)
        db = Database()
        db.update_plant(plant, user_id)
    except (InvalidId, TypeError):
        raise DbError('Invalid plant id') 


@plants.route('/plant/<identifier>', methods=['DELETE'])
@confirmation_required
def delete_plant(user_id: ObjectId, identifier: str):
    try:
        plant = Plant({'status': 'deleted'})
        plant.id = ObjectId(identifier)
        db = Database()
        db.update_plant(plant, user_id)
    except (InvalidId, TypeError):
        raise DbError('Invalid plant id') 