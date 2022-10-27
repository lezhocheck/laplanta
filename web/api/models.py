from abc import ABC, abstractmethod
from .utils import ValidationError, InvalidFormatError, regex_dict
from cerberus import Validator
from bson.objectid import ObjectId


class BaseDto(ABC):
    def __init__(self, obj: dict) -> None:
        id = obj.get('_id')
        self.id = ObjectId(id) if id else None

    @staticmethod
    def validate(schema: dict, obj: dict) -> None:
        validator = Validator(schema)
        if not validator.validate(obj):
            raise InvalidFormatError(validator)   

    @abstractmethod
    def to_dict_row(self) -> dict:
        raise NotImplementedError()

    def to_dict_guaranteed(self) -> dict:
        values_dict = self.to_dict_row()
        if any(map(lambda v: v is None, values_dict.values())):
            raise ValidationError()
        return values_dict    

    def to_dict(self) -> dict:
        values_dict = self.to_dict_row()
        filtered = {k: v for k, v in values_dict.items() 
            if v is not None}
        if not len(filtered):
            raise ValidationError()
        return filtered    

    def to_dict_with_id(self) -> dict:
        result = self.to_dict_row()
        result['_id'] = str(self.id)
        return result    


class User(BaseDto):
    def __init__(self, obj: dict) -> None:
        super().__init__(obj)
        self.email = obj.get('email')
        self.password = obj.get('password')
        self.name = obj.get('name')
        self.telephone = obj.get('telephone')
        self.account_created = obj.get('account_created') 
        self.confirmation_date = obj.get('confirmation_date')

    @staticmethod
    def from_signup_form(obj: dict) -> 'User':
        schema = {
            'email': {'type': 'string', 
                'regex': regex_dict['user']['email'], 'required': True}, 
            'password': {'type': 'string', 'required': True},
            'name': {'type': 'string', 
                'regex': regex_dict['user']['name'], 'required': True},
            'telephone': {'type': 'string', 
                'regex': regex_dict['user']['telephone'], 'required': True}
        }
        BaseDto.validate(schema, obj)
        return User(obj) 

    @staticmethod
    def from_login_form(obj: dict) -> 'User':
        schema = {
            'email': {'type': 'string', 
                'regex': regex_dict['user']['email'], 'required': True}, 
            'password': {'type': 'string', 'required': True}
        }
        BaseDto.validate(schema, obj)
        return User(obj)     

    @staticmethod
    def from_update_form(obj: dict) -> 'User':
        schema = {
            'password': {'type': 'string'},
            'name': {'type': 'string', 
                'regex': regex_dict['user']['name']},
            'telephone': {'type': 'string', 
                'regex': regex_dict['user']['telephone']}
        }
        BaseDto.validate(schema, obj)
        return User(obj) 

    def to_dict_row(self) -> dict:
        return {
            'email': self.email, 
            'password': self.password,
            'name': self.name,
            'telephone': self.telephone,
            'account_created': self.account_created,
            'confirmation_date': self.confirmation_date
        }  


class Plant(BaseDto):
    def __init__(self, obj: dict) -> None:
        super().__init__(obj)
        self.name = obj.get('name')
        self.description = obj.get('description')
        self.image_path = obj.get('image_path')
        self.status = obj.get('status')
        self.added_date = obj.get('added_date')

    @staticmethod
    def from_input_form(obj: dict) -> 'Plant': 
        schema = {'name': {'type': 'string', 'required': True},
            'description': {'type': 'string', 'nullable': True},
            'image_path': {'type': 'string', 'nullable': True},
        }
        BaseDto.validate(schema, obj)
        return Plant(obj) 
 
    @staticmethod
    def from_update_form(obj: dict) -> 'Plant': 
        schema = {'name': {'type': 'string'},
            'description': {'type': 'string'},
            'image_path': {'type': 'string'},
            'status': {'type': 'string'}
        }
        BaseDto.validate(schema, obj)
        return Plant(obj) 

    def to_dict_row(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'image_path': self.image_path,
            'status': self.status,
            'added_date': self.added_date
        }


class Sensor(BaseDto):
    def __init__(self, obj: dict) -> None:
        super().__init__(obj)
        self.name = obj.get('name')
        self.type = obj.get('type')
        self.status = obj.get('status')
        self.last_data_sent = obj.get('last_data_sent')
        self.added_date = obj.get('added_date')
        self.plants = obj.get('plants')

    @staticmethod
    def from_input_form(obj: dict) -> 'Sensor': 
        schema = {
            'name': {'type': 'string', 'required': True},
            'type': {'type': 'string', 'required': True},
            'plants': {'type': 'list', 'schema': {'type': 'string'},
                'minlength': 1, 'required': True}
        }
        if not len(set(obj['plants'])):
            raise ValidationError()
        BaseDto.validate(schema, obj)
        return Sensor(obj)

    @staticmethod
    def from_update_form(obj: dict) -> 'Sensor': 
        schema = {'name': {'type': 'string'}, 'status': {'type': 'string'}}
        BaseDto.validate(schema, obj)
        return Plant(obj) 

    def to_dict_row(self) -> dict:
        return {
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'last_data_sent': self.last_data_sent,
            'added_date': self.added_date,
            'plants': [str(p) for p in self.plants] if self.plants else None
        } 


class Record(BaseDto):
    def __init__(self, obj: dict) -> None:
        super().__init__(obj)
        self.sensor_id = ObjectId(obj.get('sensor_id'))
        self.sensor_status = obj.get('sensor_status')
        self.date = obj.get('date')
        self.value = obj.get('value')

    @staticmethod
    def from_input_form(obj: dict) -> 'Record': 
        schema = {'value': {'required': True}}
        BaseDto.validate(schema, obj)
        return Record(obj)

    def to_dict_row(self) -> dict:
        return {
            'sensor_id': str(self.sensor_id),
            'sensor_status': self.sensor_status,
            'value': self.value,
            'date': self.date
        }     