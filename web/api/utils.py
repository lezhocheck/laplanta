from enum import IntEnum
from typing_extensions import Never
from abc import ABC, abstractproperty
from cerberus import Validator
from functools import wraps
from flask import jsonify

regex_dict = {
    'user': {
         # RFC5322-compliant Regular Expression
        'email': r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])",
        
        'name': r"^[a-zA-Z0-9._'ЁёА-Яа-я іІґҐїЇЄє]{1,50}$",
        'telephone': r"^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$",
        'sensor_id': r"^[a-zA-Z0-9]{3, 100}$"
    }
}


class ResponseError(Exception, ABC):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @abstractproperty
    def status_code(self) -> int:
        raise NotImplementedError()


class InvalidFormatError(ResponseError):
    def __init__(self, validator: Validator) -> None:
        self.validator = validator
        values = self.validator.errors
        super().__init__(f'Invalid or missing parameters: {values.keys()}')

    @property
    def status_code(self) -> int:
        return 301


class DbError(ResponseError):
    def __init__(self, message) -> None:
        super().__init__(message)

    @property
    def status_code(self) -> int:
        return 302


class TokenError(ResponseError):
    def __init__(self, message) -> None:
        super().__init__(message)

    @property
    def status_code(self) -> int:
        return 303        


def _validate(handlers: dict) -> None:
    for key, value in handlers.items():
        if not issubclass(key, Exception) or not isinstance(value, str):
            raise Exception(f'Invalid dict object')



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
    return decorated
