from flask import Blueprint, request, jsonify
from .auth import confirmation_required, login_required, Database
from .models import UserDto
from .utils import DbError
from cerberus import Validator
from datetime import datetime
from .utils import regex_dict, exception_handler

sensors = Blueprint('sensors', __name__)

@sensors.route('/sensor', methods=['POST'])
@confirmation_required
@exception_handler
def register_sensor(user: UserDto, **kwargs):
    db = Database()
    schema = {'sensor_id': {'type': 'string', 'required': True,
        'regex': regex_dict['user']['sensor_id']}}
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
 

@sensors.route('/sensor/<identifier>')
@confirmation_required
@exception_handler
def get_sensor(user: UserDto, identifier: str, **kwargs):
    db = Database()
    value, _ = db.get_sensor(user, identifier)
    return value


@sensors.route('/sensor/<identifier>', methods=['DELETE'])
@confirmation_required
@exception_handler
def delete_sensor(user: UserDto, identifier: str, **kwargs):
    db = Database()
    _, index = db.get_sensor(user, identifier) 
    db.user_collection.update_one({'email': user.email}, 
        {'$set': {f'sensors.{index}.status': 'deleted'}})


@sensors.route('/sensor/<identifier>', methods=['PUT'])
@confirmation_required
@exception_handler
def update_sensor(user: UserDto, identifier: str, **kwargs):
    db = Database()
    sensor, index = db.get_sensor(user, identifier)
    schema = {'status': {'type': 'string', 'required': True, 'forbidden': [sensor['status']]}}
    validator = Validator(schema)
    input_value = request.json
    if not validator.validate(input_value):
        raise DbError(f'invalid values: {validator.errors.keys()}')  
    db.user_collection.update_one({'email': user.email}, 
        {'$set': {f'sensors.{index}.status': input_value['status']}})    


# TODO
@sensors.route('/plant/<plant_id>/record', methods=['POST'])
def add_sensor_record(user: UserDto, plant_id: int, **kwargs):
    pass
    

# TODO
@sensors.route('/sensors/<plant_id>', methods=['POST'])
@login_required
def get_sensor_records(user: UserDto, plant_id: int, **kwargs):
    db = Database()
    users =  db.get_db()
    plant = users.find_one({'email': user.email, 'plants._id': plant_id}, {'_id': 0, 'plants': 1})
    if not plant:
        raise DbError('Plant do not exist')
    return jsonify({'message': plant['sensors']}), 200    