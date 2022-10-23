from flask import request, jsonify, url_for, current_app
from flask import Blueprint
from .utils import ResponseError, DbError, exception_handler
from functools import wraps
from .database import Database, UserExtendedDto, UserDto, Token
from api import serializer, mail
from flask_mail import Message
from itsdangerous import SignatureExpired
from werkzeug.security import generate_password_hash
from cerberus import Validator

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


def confirmation_required(func):
    @wraps(func)
    @login_required
    def decorated(*args, **kwargs):
        try:
            if not isinstance(args[0], UserDto):
                raise DbError('Expecteed user')
            db = Database()
            date = db.get_confirmation_date(args[0].email)
            if date is None:
                raise DbError('User is not confirmed')
            kwargs['confirmation_date'] = date  
            return func(*args, **kwargs)
        except ResponseError as e:
            return jsonify({'message': str(e)}), e.status_code      
    return decorated


@auth.route('/user/signup', methods=['POST'])
@exception_handler
def signup():
    user = UserExtendedDto(request.json)
    db = Database()
    db.insert_user(user)


@auth.route('/user/login', methods=['POST'])
@exception_handler
def login():
    user = UserDto(request.json)
    db = Database()
    token = db.get_token_from_user(user)
    return {'token': token.encode()}


@auth.route('/user/confirm', methods=['GET', 'POST'])
@login_required
@exception_handler
def confirm_email(user: UserDto):
    email = user.email
    token = serializer.dumps(email, salt=current_app.config['PASSWORD_SALT'])
    msg = Message('Confirm your email', sender=current_app.config['MAIL_USERNAME'],
        recipients=[email])
    link = url_for(f'{auth.name}.{verify_email.__name__}', token=token, _external=True)   
    msg.body = f'Your confirmation link is {link}'    
    mail.send(msg)


@auth.route('/user/verify/<token>')
@exception_handler
def verify_email(token):
    try:
        email = serializer.loads(token, salt=current_app.config['PASSWORD_SALT'], max_age=180)
        db = Database()
        db.confirm_user_email(email)
    except SignatureExpired:
        raise DbError('Invalid link') 


@auth.route('/user')
@login_required
@exception_handler
def get_user(user: UserDto):
    db = Database()
    filter = {'_id': 0, 'password': 0, 'plants': 0, 'plants_count': 0}
    user_obj = db.find_user(user, filter)
    if not user_obj:
        raise DbError('An error occured')
    return {'user': user_obj}  


@auth.route('/user', methods=['PUT'])
@login_required
@exception_handler
def update_user(user: UserDto):
    schema = UserExtendedDto.get_schema_extention()
    schema['password'] = {'type': 'string'}
    validator = Validator(schema)
    input_value = request.json
    if not validator.validate(input_value):
        raise DbError(f'invalid values: {validator.errors.keys()}')
    filtered = {k: v for k, v in input_value.items() if v is not None}
    if not len(filtered):
        raise DbError('Cannot update')
    if 'password' in filtered:
        password = filtered['password'] 
        filtered['password'] = generate_password_hash(password) 
    db = Database()
    db.user_collection.update_one({'email': user.email}, 
        {'$set': filtered})

