from abc import ABC, abstractmethod, abstractproperty
from typing_extensions import Never
from api.utils import InvalidFormatError, regex_dict
from cerberus import Validator
from werkzeug.security import generate_password_hash

class AbstractDto(ABC):
    def __init__(self, obj: dict) -> None:
        validator = Validator(self._validation_schema)
        if not validator.validate(obj):
            raise InvalidFormatError(validator)

    @abstractmethod
    def convert_to_dict(self) -> dict:
        raise NotImplementedError()

    @abstractproperty
    def _validation_schema(self) -> dict:    
        raise NotImplementedError()


class UserDto(AbstractDto):
    def __init__(self, obj: dict) -> None:
        super().__init__(obj)
        self.email = obj.get('email')
        self.password = obj.get('password')

    @property
    def hashed_password(self):
        return generate_password_hash(self.password)    

    @property
    def _validation_schema(self) -> dict: 
        return {
            'email': {'type': 'string', 
                        'regex': regex_dict['user']['email'], 
                        'required': True
                    }, 
            'password': {'type': 'string', 'required': True}
        }

    def convert_to_dict(self) -> dict:
        return {
            'email': self.email, 
            'password': self.password
        }    
            
        
class UserExtendedDto(UserDto):
    def __init__(self, obj: dict) -> None:
        super().__init__(obj)  
        self.name = obj.get('name')
        self.telephone = obj.get('telephone')           

    @classmethod
    def get_schema_extention(cls) -> dict:
        return {
        'name': {'type': 'string', 'regex': regex_dict['user']['name']},
        'telephone': {'type': 'string', 'regex': regex_dict['user']['telephone']}
    }

    @property
    def _validation_schema(self) -> dict: 
        basic = super()._validation_schema
        extention = UserExtendedDto.get_schema_extention()
        for param in extention:
            param['required'] = True
        basic.update(extention)    
        return basic
 
    def convert_to_dict(self) -> dict:
        basic = super().convert_to_dict()
        basic['name'] = self.name
        basic['telephone'] = self.telephone
        return basic 



class PlantDto(AbstractDto):
    def __init__(self, obj: dict, user: UserDto) -> None:
        super().__init__(obj) 
        self.name = obj.get('name')
        self.description = obj.get('description')
        self.image_path = obj.get('image_path')
        self.user = user

    @property
    def _validation_schema(self) -> dict: 
        return {'name': {'type': 'string', 'required': True},
            'description': {'type': 'string', 'nullable': True, 'required': True},
            'image_path': {'type': 'string', 'nullable': True, 'required': True}
        }
 
    def convert_to_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'image_path': self.image_path
        }


class PlantExtendedDto(PlantDto):
    def __init__(self, obj: dict, user: UserDto, **kwargs) -> None:
        self._required = kwargs['required'] if 'required' in kwargs else False    
        super().__init__(obj, user)
        self.is_active = obj.get('is_active')

    @property
    def _validation_schema(self) -> dict: 
        basic = super()._validation_schema
        basic['is_active'] = {'type': 'boolean', 'required': True}
        for k in basic.keys():
            basic[k]['required'] = self._required
        return basic
 
    def convert_to_dict(self) -> dict:
        basic = super().convert_to_dict()
        basic['is_active'] = self.is_active
        return basic  


class PlantResponseDto(PlantExtendedDto):
    def __init__(self, obj: dict, user: UserDto) -> None:
        super().__init__(obj, user)
        self.id = obj.get('id')

    @property
    def _validation_schema(self) -> dict: 
        basic = super()._validation_schema
        basic['id'] = {'type': 'integer', 'required': True}
        return basic
 
    def convert_to_dict(self) -> dict:
        basic = super().convert_to_dict()
        basic['id'] = self.id
        return basic     


class SensorRecord(AbstractDto):
    def __init__(self, value) -> None:
        pass


