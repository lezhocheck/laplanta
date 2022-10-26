from bson.errors import InvalidId
from pymongo import MongoClient
from .models import *
from .utils import DbError, TokenError
from werkzeug.security import generate_password_hash
import jwt
from bson.json_util import dumps, loads
from datetime import datetime, timedelta
from flask import current_app
from bson.objectid import ObjectId
from typing import TypeVar, Union


TokenType = TypeVar('TokenType', bound='IdToken')


class IdToken:
    _ENCODING_ALGO = 'HS256'

    def __init__(self, id: ObjectId, expire_date: datetime) -> None:
        self.id = id
        self.expire_date = expire_date

    def encode(self) -> str:
        key = IdToken._get_key()
        obj = {'id': str(self.id), 'expire': dumps(self.expire_date)}
        return jwt.encode(obj, key, algorithm=IdToken._ENCODING_ALGO) 

    @staticmethod
    def decode(token: str) -> TokenType:
        key = IdToken._get_key()
        decoded = jwt.decode(token, key, algorithms=[IdToken._ENCODING_ALGO])
        user_id = ObjectId(decoded['id'])
        expire_date = loads(decoded['expire'])
        current_time = datetime.utcnow()
        if not user_id or not expire_date or current_time >= expire_date:
            raise TokenError('Token is not valid') 
        return IdToken(user_id, expire_date) 

    @staticmethod
    def create(id: ObjectId):
        expire_date = datetime.utcnow() + timedelta(minutes=30)
        return IdToken(id, expire_date)           

    @staticmethod
    def _get_key() -> str:   
        if 'SECRET_KEY' not in current_app.config:
            raise TokenError('An error occured on encoding or decoding') 
        return current_app.config['SECRET_KEY']                


class Database:
    def __init__(self) -> None:
        self._client = MongoClient('mongodb://db:27017/',
                    username='admin', 
                    password='password',
                    authMechanism='SCRAM-SHA-1')
        self._db = self._client['laplanta']

    @property
    def user_collection(self):
        return self._db['users']    

    def insert_user(self, user: User) -> ObjectId:
        if self.user_exists(user.email):
            raise DbError('User already exists')
        user.account_created = datetime.utcnow()
        user.password = generate_password_hash(user.password)      
        record = user.to_dict_row()
        record.update({'plants': [], 'sensors': [], 'records': []})    
        result = self.user_collection.insert_one(record)   
        return result.inserted_id

    def user_exists(self, value: Union[str, ObjectId]) -> bool:
        try:
            _ = self.get_user(value)
            return True
        except DbError:
            return False

    def get_user(self, value: Union[str, ObjectId]) -> User:
        value = self.user_collection.find_one({'$or': [{'_id': value}, {'email': value}]})
        if not value:
            raise DbError('User does not exist')
        return User(value)    

    def update_user(self, user: User) -> None:
        if not self.user_exists(user.email) and not self.user_exists(user.id):
            raise DbError('User does not exist')  
        record = user.to_dict() 
        if 'password' in record:
            record['password'] = generate_password_hash(record['password'])   
        update_rule = {'$or': [{'_id': user.id}, {'email': user.email}]}
        result = self.user_collection.update_one(update_rule, {'$set': record})     
        if not result:
            raise DbError('User update failed')
    
    def insert_plant(self, plant: Plant, user_id: ObjectId) -> ObjectId:
        if not self.user_exists(user_id):
            raise DbError('User does not exist')
        plant_obj = plant.to_dict_row()
        id = ObjectId()
        plant_obj.update({'records': [], 'status': 'ok', 
            '_id': id, 'added_date': datetime.utcnow()})
        self.user_collection.update_one({'_id': user_id}, 
            {'$push': {'plants': plant_obj}})  
        return id        

    def get_plants(self, user_id: ObjectId) -> list[Plant]:
        plants = self.user_collection.find({'_id': user_id}, {'_id': 0, 'plants': 1})
        if not plants:
            raise DbError('User not found') 
        result = list(plants)  
        if not len(result):
            raise DbError('No plants found') 
        return [Plant(i) for i in result[0]['plants']]

    def get_plant_by_id(self, plant_id: ObjectId) -> Plant:
        result = self.user_collection.find_one({'plants._id': plant_id}, {'plants.$': 1, '_id': 0})   
        if not result:
            raise DbError('Plant not found') 
        if len(result['plants']) != 1:
            raise DbError('Invalid plant id')
        return Plant(result['plants'][0])
            
    def update_plant(self, plant: Plant, user_id: ObjectId) -> None:
        plant_obj = plant.to_dict()
        setter = {f'plants.$.{k}': v for k, v in plant_obj.items()}
        result = self.user_collection.update_one({'_id': user_id, 
            'plants._id': plant.id}, {'$set': setter})
        if not result:
            raise DbError('Invalid data')   

    def insert_sensor(self, sensor: Sensor, user_id: ObjectId) -> None:
        if not self.user_exists(user_id):
            raise DbError('User does not exist')
        try:    
            for p in sensor.plants:
                _ = self.get_plant_by_id(ObjectId(p))
        except (InvalidId, TypeError):
            raise DbError('Invalid plants id')  
        sensor_obj = sensor.to_dict_row()
        id = ObjectId()
        sensor_obj.update({'status': 'working',
            '_id': id, 'added_date': datetime.utcnow()})
        self.user_collection.update_one({'_id': user_id}, 
            {'$push': {'sensors': sensor_obj}})  
        return id   

    def get_sensors(self, user_id: ObjectId) -> list[Sensor]:
        sensors = self.user_collection.find({'_id': user_id}, {'_id': 0, 'sensors': 1})
        if not sensors:
            raise DbError('User not found') 
        result = list(sensors)  
        if not len(result):
            raise DbError('No sensors found') 
        return [Sensor(i) for i in result[0]['sensors']]    

    def update_sensor(self, sensor: Sensor, user_id: ObjectId) -> None:
        sensor_obj = sensor.to_dict()
        setter = {f'sensors.$.{k}': v for k, v in sensor_obj.items()}
        result = self.user_collection.update_one({'_id': user_id, 
            'sensors._id': sensor.id}, {'$set': setter})
        if not result:
            raise DbError('Invalid data')     

    def get_sensor_by_id(self, sensor_id: ObjectId) -> Sensor:
        result = self.user_collection.find_one({'sensors._id': sensor_id}, {'sensors.$': 1, '_id': 0})   
        if not result:
            raise DbError('Sensor not found') 
        if len(result['sensors']) != 1:
            raise DbError('Invalid sensor id')
        return Sensor(result['sensors'][0])       

    def get_record_by_id(self, record_id: ObjectId) -> Sensor:
        result = self.user_collection.find_one({'records._id': record_id}, {'records.$': 1, '_id': 0})   
        if not result:
            raise DbError('Record not found') 
        if len(result['records']) != 1:
            raise DbError('Invalid record id')
        return Record(result['records'][0])      
            
    def insert_record(self, record: Record) -> ObjectId:
        sensor = self.get_sensor_by_id(record.sensor_id)
        if sensor.status in ['deleted']:
            raise DbError('Sensor is deleted')
        user_obj = self.user_collection.find_one({'sensors._id': record.sensor_id}, {'_id': 1})
        if not user_obj:
            raise DbError('Invalid data')    
        record.date = datetime.utcnow()
        record.sensor_id = ObjectId(record.sensor_id)
        record.sensor_status = sensor.status    
        record_obj = record.to_dict_row()  
        record_obj['_id'] = ObjectId()
        self.user_collection.update_one({'_id': user_obj['_id'], 'sensors._id': sensor.id}, 
            {'$push': {'records': record_obj}, '$set': {'sensors.$.last_data_sent': datetime.utcnow()}})
        for p in sensor.plants:
            self.user_collection.update_one({'_id': user_obj['_id'], 'plants._id': ObjectId(p)},
                {'$push': {f'plants.$.records': record_obj['_id']}})

    def get_records(self, user_id: ObjectId) -> list[Record]:
        records = self.user_collection.find({'_id': user_id}, {'_id': 0, 'records': 1})
        if not records:
            raise DbError('User not found') 
        result = list(records)  
        if not len(result):
            raise DbError('No records found') 
        return [Record(i) for i in result[0]['records']]                     

    def get_records_by_plant(self, plant_id: ObjectId) -> list:
        result = self.user_collection.find_one({'plants._id': plant_id}, 
            {'plants.$': 1, '_id': 0})
        if not result:
            raise DbError('Plant not found') 
        if len(result['plants']) != 1:
            raise DbError('Invalid plant id')
        record_list = result['plants'][0]['records']
        return [self.get_record_by_id(id) for id in record_list]