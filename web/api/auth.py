from flask import request, url_for, current_app
from flask import Blueprint
from .utils import ValidationError, exception_handler
from functools import wraps
from .database import Database, User
from api import serializer, mail
from flask_mail import Message
from itsdangerous import SignatureExpired
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash
from datetime import datetime
from .token import IdToken, TokenError


auth = Blueprint('auth', __name__)


def login_required(func):
    @wraps(func)
    @exception_handler
    def decorated(*args, **kwargs):
        if 'x-access-token' not in request.headers:
            raise TokenError('Token is missing')
        token = IdToken.decode(request.headers['x-access-token'])
        db = Database()
        if not db.user_exists(token.id):
            raise ValidationError(['token'])
        return func(token.id, *args, **kwargs)    
    return decorated


def confirmation_required(func):
    @wraps(func)
    @login_required
    def decorated(user_id: ObjectId, *args, **kwargs):
        db = Database()
        date = db.get_user(user_id).confirmation_date
        if date is None:
            raise ValidationError(['confirmation'])
        return func(user_id, *args, **kwargs)   
    return decorated


@auth.route('/user/signup', methods=['POST'])
@exception_handler
def signup():
    user = User.from_signup_form(request.json)
    db = Database()
    id = db.insert_user(user)
    return {'user_id': str(id)}


@auth.route('/user/login', methods=['POST'])
@exception_handler
def login():
    user_input = User.from_login_form(request.json)
    db = Database()
    user_data = db.get_user(user_input.email)
    if not check_password_hash(user_data.password, user_input.password):
        raise ValidationError(['password'])     
    token = IdToken.create(user_data.id)
    return {'token': token.encode()}


@auth.route('/user/confirmation', methods=['POST'])
@login_required
def send_confirmation(user_id: ObjectId):
    db = Database()
    user = db.get_user(user_id)
    if user.confirmation_date:
        raise TokenError('User is already confirmed')
    token = serializer.dumps(user.email, salt=current_app.config['PASSWORD_SALT'])
    msg = Message('Confirm your email', sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email])
    link = url_for(f'{auth.name}.{get_confirmation.__name__}', token=token, _external=True)   
    msg.body = f'Your confirmation link is {link}'    
    mail.send(msg)


@auth.route('/user/confirmation/<token>')
@exception_handler
def get_confirmation(token: str):
    try:
        email = serializer.loads(token, salt=current_app.config['PASSWORD_SALT'], max_age=360)
        db = Database()
        db_user = db.get_user(email)
        if db_user.confirmation_date:
            raise TokenError('User is already confirmed')    
        updatation_user = User({'_id': db_user.id, 
            'email': email, 'confirmation_date': datetime.utcnow()})
        db.update_user(updatation_user)
    except SignatureExpired:
        raise TokenError('Invalid link') 


@auth.route('/user')
@login_required
def get_user(user_id: ObjectId):
    db = Database()
    user = db.get_user(user_id)
    user_obj = user.to_dict_row()
    user_obj.pop('password')
    return {'user': user_obj}  


@auth.route('/user', methods=['PUT'])
@login_required
def update_user(user_id: ObjectId):
    input_user = User.from_update_form(request.json)
    obj = input_user.to_dict()
    if not len(obj):
        raise ValidationError()
    obj['_id'] = user_id  
    db = Database()
    db.update_user(User(obj))

