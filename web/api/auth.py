from flask import request, jsonify
from flask import Blueprint
from .utils import ResponseError
from functools import wraps
from .database import Database, UserExtendedDto, UserDto, Token


auth = Blueprint('auth', __name__)


def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if 'x-access-token' not in request.headers:
             return jsonify({'message': 'Token is missing'}), 401
        try:
            token = Token.decode(request.headers['x-access-token'])
            db = Database()
            user = db.get_user_from_token(token)
            return func(user, *args, **kwargs)
        except ResponseError as e:
            return jsonify({'message': str(e)}), e.status_code     
    return decorated


@auth.route('/signup', methods=['POST'])
def signup():
    try:    
        user = UserExtendedDto(request.json)
        db = Database()
        db.insert_user(user)
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code
    return jsonify({'message': 'Success'}), 200


@auth.route('/login', methods=['POST'])
def login():
    try:
        user = UserDto(request.json)
        db = Database()
        token = db.get_token_from_user(user)
        return jsonify({'message': token.encode()}), 200
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code
