from abc import ABC, abstractproperty
from cerberus import Validator
from functools import wraps
from flask import jsonify
from bson.errors import InvalidId
from typing import Union


regex_dict = {
    'user': {
         # RFC5322-compliant Regular Expression
        'email': r"^([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])$",
        'name': r"^[a-zA-Z0-9._'ЁёА-Яа-я іІґҐїЇЄє]{1,50}$",
        'telephone': r"^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
    }
}


class ResponseError(Exception, ABC):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @abstractproperty
    def status_code(self) -> int:
        raise NotImplementedError()


class ValidationError(ResponseError):
    def __init__(self, errors: Union[list[str], None] = None) -> None:
        message = f'Invalid or missing parameters'
        additional = '' if errors is None else f': {errors}'
        super().__init__(message + additional)

    @property
    def status_code(self) -> int:
        return 501   


class InvalidFormatError(ValidationError):
    def __init__(self, validator: Validator) -> None:
        values = validator.errors
        super().__init__(list(values.keys())) 


def exception_handler(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:
                return jsonify({'message': 'Success'}), 200
            return jsonify({'message': result}), 200   
        except ResponseError as e:
            return jsonify({'message': str(e)}), e.status_code    
        except InvalidId:
            return jsonify({'message': 'Invalid id passed'}), 504                 
    return decorated
