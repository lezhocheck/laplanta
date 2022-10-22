from enum import IntEnum
from typing_extensions import Never
from abc import ABC, abstractproperty
from cerberus import Validator


regex_dict = {
    'user': {
         # RFC5322-compliant Regular Expression
        'email': r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])",
        
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