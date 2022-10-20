from turtle import update
from pymongo import MongoClient
from .models import PlantExtendedDto, UserDto, UserExtendedDto, PlantDto, PlantResponseDto
from .utils import DbError, TokenError
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from bson.json_util import dumps, loads
from datetime import datetime, timedelta
from flask import current_app
from bson.objectid import ObjectId
from typing import TypeVar


TokenType = TypeVar('TokenType', bound='Token')


class Token:
    _ENCODING_ALGO = 'HS256'

    def __init__(self, user_id: ObjectId, expire_date: datetime) -> None:
        self.user_id = user_id
        self.expire_date = expire_date

    def encode(self) -> str:
        key = Token._get_key()
        obj = {'id': str(self.user_id), 'expire': dumps(self.expire_date)}
        return jwt.encode(obj, key, algorithm=Token._ENCODING_ALGO) 

    @staticmethod
    def decode(token: str) -> TokenType:
        key = Token._get_key()
        decoded = jwt.decode(token, key, algorithms=[Token._ENCODING_ALGO])
        user_id = ObjectId(decoded['id'])
        expire_date = loads(decoded['expire'])
        if not user_id or not expire_date:
            raise TokenError('Token is not valid') 
        return Token(user_id, expire_date)    

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

    def insert_user(self, user: UserExtendedDto) -> None:
        if self.find_user(user):
            raise DbError('User already exists')
        record = user.convert_to_dict()
        additional_info = {
            'password': user.hashed_password,
            'account_created': datetime.utcnow(),
            'confirmed': False,
            'confirmed_on': None,
            'plants': [],
            'plants_count': 0
        }
        record.update(additional_info)    
        self.user_collection.insert_one(record)   

    def get_token_from_user(self, user: UserDto) -> TokenType:
        user_record = self.find_user(user)
        if not user_record:
            raise DbError('User does not exist')    
        if not check_password_hash(user_record['password'], user.password):
            raise DbError('Invalid password') 
        expire_date = datetime.utcnow() + timedelta(minutes=30)
        return Token(user_record['_id'], expire_date)      

    def get_user_from_token(self, token: TokenType) -> UserDto:
        current_time = datetime.utcnow()
        if current_time >= token.expire_date:
            raise TokenError('Token is not valid') 
        filter = {'_id': 0, 'email': 1, 'password': 1}
        user = self.user_collection.find_one({'_id': token.user_id}, filter) 
        if not user:
            raise TokenError('Token is not valid')  
        return UserDto(user)   

    def confirm_user_email(self, user_email: str) -> None:
        user = self.user_collection.find_one({'email': user_email})
        if not user or not all(i in user for i in ('confirmed', 'confirmed_on')):
            raise DbError('An error occured on user email confirmation')
        if user['confirmed']:
            raise DbError('User email already confirmed')
        setter = {'$set': {'confirmed': True, 'confirmed_on': datetime.utcnow()}}    
        self.user_collection.update_one({'_id': user['_id']}, setter)    

    def find_user(self, user: UserDto, filter: dict = None) -> dict:
        return self.user_collection.find_one({'email': user.email}, filter)

    def get_confirmation_date(self, user_email: str) -> datetime | None:
        user = self.user_collection.find_one({'email': user_email})
        if not user or not all(i in user for i in ('confirmed', 'confirmed_on')):
            raise DbError('An error occured on getting information')
        return user['confirmed_on']

    def add_plant(self, plant: PlantDto) -> int:
        user = self.find_user(plant.user)
        if not user:
            raise DbError('An error occured on posting information')
        plant_obj = plant.convert_to_dict()
        additional_info = {
            '_id': user['plants_count'],
            'is_active': True,
            'sensors': []
        }
        plant_obj.update(additional_info)
        new_id = user['plants_count']
        upd = {'$push': {'plants': plant_obj}, '$set': {'plants_count': new_id + 1}}
        self.user_collection.update_one({'email': plant.user.email}, upd)    
        return new_id

    def get_plant(self, user: UserDto, plant_id: int) -> PlantResponseDto:
        user_record = self.user_collection.find_one({'email': user.email})
        if not user_record:
            raise DbError('An error occured on posting information')
  
        if plant_id < 0 or plant_id >= user_record['plants_count']:
            raise DbError('No plant with such id')
        plant_obj = user_record['plants'][plant_id]   
        plant_obj.pop('sensors')
        plant_obj['id'] = plant_obj.pop('_id')
        return PlantResponseDto(plant_obj, user)

    def update_plant(self, plant: PlantExtendedDto, plant_id: int) -> None:
        user = self.user_collection.find_one({'email': plant.user.email})
        if not user:
            raise DbError('An error occured on updating information')
        if plant_id < 0 or plant_id >= user['plants_count']:
            raise DbError('No plant with such id')
        plant_obj = user['plants'][plant_id]
        new_data = plant.convert_to_dict()
        filtered = {k: v for k, v in new_data.items() if v is not None}
        plant_obj.update(filtered)    
        self.user_collection.update_one({'_id': user['_id']}, 
            {'$set': {f'plants.{plant_id}': plant_obj}})

    def delete_plant(self, user: UserDto, plant_id: int) -> None:
        plant = self.get_plant(user, plant_id)
        plant_obj = plant.convert_to_dict()
        plant_obj.pop('id') 
        plant_obj['is_active'] = False
        self.update_plant(PlantExtendedDto(plant_obj, user), plant_id)       

         