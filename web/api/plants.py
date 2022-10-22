from inspect import indentsize
from flask import Blueprint, request, jsonify
from .auth import confirmation_required, login_required, Database
from .models import UserDto, PlantDto, PlantExtendedDto
from .utils import DbError, ResponseError
from cerberus import Validator
from datetime import datetime


plants = Blueprint('plants', __name__)


@plants.route('/plant', methods=['POST'])
@confirmation_required
def add_plant(user: UserDto, **kwargs):
    try:
        plant = PlantDto(request.json, user)
        db = Database()
        id = db.add_plant(plant)
        return jsonify({'message': {'result': 'You successfuly added a plant', 'id': id}}), 200 
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code      


@plants.route('/plant/<plant_id>')
@confirmation_required
def get_plant(user: UserDto, plant_id: int, **kwargs):
    try:
        db = Database()
        plant = db.get_plant(user, int(plant_id))
        return jsonify({'message': plant.convert_to_dict()}), 200
    except ValueError:
        return jsonify({'message': 'Invalid plant id'}), 402        
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code     


@plants.route('/plant/<plant_id>', methods=['PUT'])
@confirmation_required
def update_plant(user: UserDto, plant_id: int, **kwargs):
    try:
        if not len(request.json):
            raise ResponseError('Cannot update with empty params')
        plant = PlantExtendedDto(request.json, user, required=False)
        db = Database()
        db.update_plant(plant, int(plant_id))
        return jsonify({'message': 'The update was successful'}), 200
    except ValueError:
        return jsonify({'message': 'Invalid plant id'}), 402    
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code     


@plants.route('/plant/<plant_id>/', methods=['DELETE'])
@confirmation_required
def delete_plant(user: UserDto, plant_id: int, **kwargs):
    try:
        db = Database()
        db.delete_plant(user, int(plant_id))
        return jsonify({'message': 'The deletion was successful'}), 200
    except ValueError:
        return jsonify({'message': 'Invalid plant id'}), 402    
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code  


@plants.route('/plants')
@confirmation_required
def get_plants(user: UserDto, **kwargs):
    try:
        db = Database()
        result = db.find_user(user, {'_id': 0, 'plants': 1})
        if not result:
            raise DbError('No plants')
        return jsonify({'message': result}), 200   
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code  


# TODO
@plants.route('/plant/<plant_id>/status')
@confirmation_required
def get_plant_status(user: UserDto, plant_id: int, **kwargs):
    pass


@plants.route('/sensor', methods=['POST'])
@confirmation_required
def register_sensor(user: UserDto, **kwargs):
    try:
        db = Database()
        schema = {'sensor_id': {'type': 'string', 'required': True}}
        validator = Validator(schema)
        input_value = request.json
        if not validator.validate(input_value):
            raise DbError(f'invalid values: {validator.errors.keys()}')
        value = db.user_collection.find_one({'email': user.email, 'sensors._id': input_value['sensor_id']})
        if value:
            raise DbError(f'Sensor is already registered')     
        info = {
            '_id': input_value['sensor_id'],
            'status': 'not accepted',
            'added': datetime.utcnow()
        }
        upd = {'$push': {'sensors': info}, '$inc': {'sensors_count': 1}}
        db.user_collection.update_one({'email': user.email}, upd)    
        return jsonify({'message': 'Success'}), 200   
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code  
 

def get_sensor_db(user: UserDto, identifier: str) -> dict:
    db = Database()
    value = db.user_collection.find_one({'email': user.email})['sensors']
    if not value:
        raise DbError(f'Sensor does not exist')
    index = -1
    for ind, t in enumerate(value):
        if t['_id'] == identifier:
            index = ind
    if index == -1:
        raise DbError(f'Sensor does not exist')            
    return value[index]

@plants.route('/sensor/<identifier>')
@confirmation_required
def get_sensor(user: UserDto, identifier: str, **kwargs):
    try:
        value = get_sensor_db(user, identifier)
        return jsonify({'message': value}), 200   
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code


# TODO
@plants.route('/sensor/<identifier>', methods=['DELETE'])
@confirmation_required
def delete_sensor(user: UserDto, identifier: str, **kwargs):
    pass


# TODO: CHANGE
@plants.route('/sensor/<identifier>', methods=['PUT'])
@confirmation_required
def update_sensor(user: UserDto, identifier: str, **kwargs):
    try:
        db = Database()
        sensor = get_sensor_db(user, identifier)
        schema = {'status': {'type': 'string', 'required': True, 'forbidden': [sensor['status']]}}
        validator = Validator(schema)
        input_value = request.json
        if not validator.validate(input_value):
            raise DbError(f'invalid values: {validator.errors.keys()}')
        sensor['status'] = input_value['status']    
        db.user_collection.update_one({'email': user.email}, 
            {'$set': {f'sensors.{identifier}': sensor}})    
        return jsonify({'message': 'Success'}), 200   
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code

@plants.route('/plant/<plant_id>/record', methods=['POST'])
def add_sensor_record(user: UserDto, plant_id: int, **kwargs):
    db = Database()
    plant = db.get_plant(user, plant_id)
    

@plants.route('/sensors/<plant_id>', methods=['POST'])
@login_required
def get_sensor_records(user: UserDto, plant_id: int, **kwargs):
    db = Database()
    users =  db.get_db()
    plant = users.find_one({'email': user.email, 'plants._id': plant_id}, {'_id': 0, 'plants': 1})
    if not plant:
        raise DbError('Plant do not exist')
    return jsonify({'message': plant['sensors']}), 200    