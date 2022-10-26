from flask import Blueprint, request
from .auth import confirmation_required, Database
from .models import Sensor, Record
from .utils import DbError
from .utils import exception_handler
from bson.objectid import ObjectId
from bson.errors import InvalidId


sensors = Blueprint('sensors', __name__)


@sensors.route('/sensor', methods=['POST'])
@confirmation_required
def add_sensor(user_id: ObjectId):
    sensor = Sensor.from_input_form(request.json)
    db = Database()
    id = db.insert_sensor(sensor, user_id)
    return {'sensor_id': str(id)}     


@sensors.route('/sensors')
@confirmation_required
def get_sensors(user_id: ObjectId):
    db = Database()
    sensors = db.get_sensors(user_id)
    def process(sensor):
        result = sensor.to_dict_row()
        result['id'] = str(sensor.id)
        return result
    sensors_obj = list(map(process, sensors))
    return {'sensors': sensors_obj}


@sensors.route('/sensor/<identifier>')
@confirmation_required
def get_sensor(user_id: ObjectId, identifier: str):
    try:
        db = Database()
        sensor = db.get_sensor_by_id(ObjectId(identifier))
        def process(sensor):
            result = sensor.to_dict_row()
            result['id'] = str(sensor.id)
            return result
        return {'sensor': process(sensor)}
    except (InvalidId, TypeError):
        raise DbError('Invalid sensor id')


@sensors.route('/sensor/<identifier>', methods=['PUT'])
@confirmation_required
def update_sensor(user_id: ObjectId, identifier: str):
    try:
        sensor = Sensor.from_update_form(request.json)
        sensor.id = ObjectId(identifier)
        db = Database()
        db.update_sensor(sensor, user_id)
    except (InvalidId, TypeError):
        raise DbError('Invalid sensor id') 


@sensors.route('/sensor/<identifier>', methods=['DELETE'])
@confirmation_required
def delete_sensor(user_id: ObjectId, identifier: str):
    try:
        sensor = Sensor({'status': 'deleted'})
        sensor.id = ObjectId(identifier)
        db = Database()
        db.update_sensor(sensor, user_id)
    except (InvalidId, TypeError):
        raise DbError('Invalid sensor id') 


@sensors.route('/sensor/<sensor_id>/record', methods=['POST'])
@exception_handler
def add_record(sensor_id: str):
    try:
        db = Database()
        record = Record.from_input_form(request.json)
        record.sensor_id = ObjectId(sensor_id)
        db.insert_record(record)    
    except (InvalidId, TypeError):
        raise DbError('Invalid sensor id') 
    

@sensors.route('/plant/<plant_id>/records')
@confirmation_required
def get_records_by_plant(user_id: ObjectId, plant_id: str):
    try:
        db = Database()
        records = db.get_records_by_plant(ObjectId(plant_id))
        def process(record):
            result = record.to_dict_row()
            result['id'] = str(record.id)
            result['sensor_id'] = str(record.sensor_id)
            return result
        records_obj = list(map(process, records))    
        return {'records': records_obj}
    except (InvalidId, TypeError):
        raise DbError('Invalid plant id') 


@sensors.route('/records')
@confirmation_required
def get_records(user_id: ObjectId):
    db = Database()
    records = db.get_records(user_id)
    def process(record):
        result = record.to_dict_row()
        result['id'] = str(record.id)
        return result
    records_obj = list(map(process, records))
    return {'records': records_obj}