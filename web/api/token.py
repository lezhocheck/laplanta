from bson.objectid import ObjectId
from datetime import datetime, timedelta
import jwt
from bson.json_util import dumps, loads
from .utils import ResponseError
from flask import current_app


class TokenError(ResponseError):
    def __init__(self, message) -> None:
        super().__init__(message)

    @property
    def status_code(self) -> int:
        return 503        


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
    def decode(token: str) -> 'IdToken':
        key = IdToken._get_key()
        decoded = jwt.decode(token, key, algorithms=[IdToken._ENCODING_ALGO])
        user_id = ObjectId(decoded['id'])
        expire_date = loads(decoded['expire'])
        current_time = datetime.utcnow()
        if not user_id or not expire_date or current_time >= expire_date:
            raise TokenError('Token is not valid') 
        return IdToken(user_id, expire_date) 

    @staticmethod
    def create(id: ObjectId) -> 'IdToken':
        expire_date = datetime.utcnow() + timedelta(minutes=30)
        return IdToken(id, expire_date)           

    @staticmethod
    def _get_key() -> str:   
        if 'SECRET_KEY' not in current_app.config:
            raise TokenError('An error occured on encoding or decoding') 
        return current_app.config['SECRET_KEY']                
