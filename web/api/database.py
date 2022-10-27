from pymongo import MongoClient
from .models import *
from .utils import ResponseError
from werkzeug.security import generate_password_hash
from datetime import datetime
from bson.objectid import ObjectId
from typing import Union
from flask import current_app
from typing import Type


class DbError(ResponseError):
    def __init__(self, message) -> None:
        super().__init__(message)

    @property
    def status_code(self) -> int:
        return 502


class Database:
    def __init__(self) -> None:
        self._client = MongoClient('mongodb://db:27017/',
                    username=current_app.config['MONGO_DB_ADMIN_USER'], 
                    password=current_app.config['MONGO_DB_ADMIN_PASSWORD'],
                    authMechanism='SCRAM-SHA-1')
        self._db = self._client['laplanta']

    @property
    def _collection(self):
        return self._db['users']    

    def insert_user(self, user: User) -> ObjectId:
        if self._user_exists(user.email):
            raise DbError('User already exists')
        user.account_created = datetime.utcnow()
        user.password = generate_password_hash(user.password)      
        record = user.to_dict_row()
        record.update({'plants': [], 'sensors': [], 'records': []})    
        result = self._collection.insert_one(record)   
        return result.inserted_id

    def user_exists(self, value: Union[str, ObjectId]) -> bool:
        try:
            _ = self.get_user(value)
            return True
        except:
            return False

    def get_user(self, value: Union[str, ObjectId]) -> User:
        value = self._collection.find_one({'$or': [{'_id': value}, {'email': value}]})
        if not value:
            raise DbError('User does not exist')
        return User(value)

    def update_user(self, user: User) -> None:
        _ = self.get_user(user.id) 
        record = user.to_dict() 
        if 'password' in record:
            record['password'] = generate_password_hash(record['password'])   
        update_rule = {'$or': [{'_id': user.id}, {'email': user.email}]}
        result = self._collection.update_one(update_rule, {'$set': record})     
        if not result:
            raise DbError('User update failed')
    
    def insert_plant(self, plant: Plant, user_id: ObjectId) -> ObjectId:
        _ = self.get_user(user_id)
        plant_obj = plant.to_dict_row()
        id = ObjectId()
        plant_obj.update({'records': [], 'status': 'ok', 
            '_id': id, 'added_date': datetime.utcnow()})
        self._collection.update_one({'_id': user_id}, 
            {'$push': {'plants': plant_obj}})  
        return id

    def get_plants(self, user_id: ObjectId) -> list[Plant]:
        return self._get_objects(Plant, user_id)

    def _get_objects(self, class_value: Type[BaseDto], user_id: ObjectId) -> list[BaseDto]:
        _, _, values_lower = Database._get_base_dto_names(class_value) 
        objects = self._collection.find({'_id': user_id}, {'_id': 0, values_lower: 1})
        if not object:
            raise DbError('User not found') 
        result = list(objects)  
        if not len(result):
            raise DbError(f'No {values_lower} found') 
        return [class_value(i) for i in result[0][values_lower]]

    def get_plant_by_id(self, plant_id: ObjectId) -> Plant:
        return self._get_by_id(Plant, plant_id)

    def _get_by_id(self, class_value: Type[BaseDto], object_id: ObjectId) -> BaseDto:
        value, value_lower, values_lower = Database._get_base_dto_names(class_value) 
        result = self._collection.find_one({f'{values_lower}._id': object_id}, 
            {f'{values_lower}.$': 1, '_id': 0})   
        if not result:
            raise DbError(f'{value} not found') 
        if len(result[values_lower]) != 1:
            raise DbError(f'Invalid {value_lower} id')
        return class_value(result[values_lower][0])

    @staticmethod
    def _get_base_dto_names(class_value: Type[BaseDto]) -> tuple[str]:
        value = class_value.__name__
        value_lower = value.lower()
        values_lower = value_lower + 's'   
        return value, value_lower, values_lower          
            
    def update_plant(self, plant: Plant, user_id: ObjectId) -> None:
        _ = self.get_plant_by_id(plant.id)
        plant_obj = plant.to_dict()
        setter = {f'plants.$.{k}': v for k, v in plant_obj.items()}
        self._collection.update_one({'_id': user_id, 
            'plants._id': plant.id}, {'$set': setter})

    def insert_sensor(self, sensor: Sensor, user_id: ObjectId) -> None:
        _ = self.get_user(user_id)
        for p in sensor.plants:
            _ = self.get_plant_by_id(ObjectId(p))
        sensor_obj = sensor.to_dict_row()
        id = ObjectId()
        sensor_obj.update({'status': 'working',
            '_id': id, 'added_date': datetime.utcnow()})
        self._collection.update_one({'_id': user_id}, 
            {'$push': {'sensors': sensor_obj}})  
        return id   

    def get_sensors(self, user_id: ObjectId) -> list[Sensor]:
        return self._get_objects(Sensor, user_id)   

    def update_sensor(self, sensor: Sensor, user_id: ObjectId) -> None:
        _ = self.get_sensor_by_id(sensor.id)
        sensor_obj = sensor.to_dict()
        setter = {f'sensors.$.{k}': v for k, v in sensor_obj.items()}
        self._collection.update_one({'_id': user_id, 
            'sensors._id': sensor.id}, {'$set': setter})

    def get_sensor_by_id(self, sensor_id: ObjectId) -> Sensor:
        return self._get_by_id(Sensor, sensor_id)

    def get_record_by_id(self, record_id: ObjectId) -> Record:
        return self._get_by_id(Record, record_id)      
            
    def insert_record(self, record: Record) -> ObjectId:
        sensor = self.get_sensor_by_id(record.sensor_id)
        if sensor.status in ['deleted']:
            raise DbError('Sensor is deleted')
        for plant_id in sensor.plants:
            plant = self.get_plant_by_id(ObjectId(plant_id))   
            if plant.status in ['deleted']:
                raise DbError('Plant is deleted')        
        user_obj = self._collection.find_one({'sensors._id': record.sensor_id}, {'_id': 1})
        if not user_obj:
            raise DbError('Invalid data')
        record.id = ObjectId()        
        record.date = datetime.utcnow()
        record.sensor_status = sensor.status    
        record_obj = record.to_dict_with_id()  
        self._collection.update_one({'_id': user_obj['_id'], 'sensors._id': sensor.id}, 
            {'$push': {'records': record_obj}, '$set': {'sensors.$.last_data_sent': datetime.utcnow()}})
        for p in sensor.plants:
            self._collection.update_one({'_id': user_obj['_id'], 'plants._id': ObjectId(p)},
                {'$push': {f'plants.$.records': record_obj['_id']}})

    def get_records(self, user_id: ObjectId) -> list[Record]:
        return self._get_objects(Record, user_id)                 

    def get_records_by_plant(self, plant_id: ObjectId) -> list[Sensor]:
        result = self._collection.find_one({'plants._id': plant_id}, 
            {'plants.$': 1, '_id': 0})
        if not result:
            raise DbError('Plant not found') 
        if len(result['plants']) != 1:
            raise DbError('Invalid plant id')
        record_list = result['plants'][0]['records']
        return [self.get_record_by_id(id) for id in record_list]