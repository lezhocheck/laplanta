from flask import Blueprint, request
from .auth import confirmation_required, Database
from .models import Sensor, Record
from .utils import exception_handler
from bson.objectid import ObjectId


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
    sensors_obj = list(map(lambda x: x.to_dict_with_id(), sensors))
    return {'sensors': sensors_obj}


@sensors.route('/sensor/<identifier>')
@confirmation_required
def get_sensor(_, identifier: str):
    db = Database()
    sensor = db.get_sensor_by_id(ObjectId(identifier))
    return {'sensor': sensor.to_dict_with_id()}


@sensors.route('/sensor/<identifier>', methods=['PUT'])
@confirmation_required
def update_sensor(user_id: ObjectId, identifier: str):
    sensor = Sensor.from_update_form(request.json)
    sensor.id = ObjectId(identifier)
    db = Database()
    db.update_sensor(sensor, user_id) 


@sensors.route('/sensor/<identifier>', methods=['DELETE'])
@confirmation_required
def delete_sensor(user_id: ObjectId, identifier: str):
    sensor = Sensor({'status': 'deleted'})
    sensor.id = ObjectId(identifier)
    db = Database()
    db.update_sensor(sensor, user_id)


@sensors.route('/sensor/<sensor_id>/record', methods=['POST'])
@exception_handler
def add_record(sensor_id: str):
    db = Database()
    record = Record.from_input_form(request.json)
    record.sensor_id = ObjectId(sensor_id)
    db.insert_record(record)    
    

@sensors.route('/plant/<plant_id>/records')
@confirmation_required
def get_records_by_plant(_, plant_id: str):
    db = Database()
    records = db.get_records_by_plant(ObjectId(plant_id))
    records_obj = list(map(lambda x: x.to_dict_with_id(), records))    
    return {'records': records_obj}

@sensors.route('/records')
@confirmation_required
def get_records(user_id: ObjectId):
    db = Database()
    records = db.get_records(user_id)
    records_obj = list(map(lambda x: x.to_dict_with_id(), records))
    return {'records': records_obj}