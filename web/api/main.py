from flask import Blueprint, current_app, url_for, jsonify, request

from .models import UserDto, PlantDto
from .auth import login_required, Database
from api import serializer, mail, app
from flask_mail import Message
from itsdangerous import SignatureExpired
from .utils import DbError, ResponseError


main = Blueprint('main', __name__)


@main.route('/verify', methods=['GET', 'POST'])
@login_required
def verify_email(user: UserDto):
    email = user.email
    token = serializer.dumps(email, salt=app.config['PASSWORD_SALT'])
    msg = Message('Confirm your email', sender=current_app.config['MAIL_USERNAME'],
        recipients=[email])
    link = url_for('main.confirm_email', token=token, _external=True)   
    msg.body = f'Your confirmation link is {link}'    
    mail.send(msg)
    return token


@main.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt=app.config['PASSWORD_SALT'], max_age=180)
        db = Database()
        db.confirm_user_email(email)
        return jsonify({'message': 'You successfuly confirmed your email'}), 200
    except SignatureExpired:
        return jsonify({'message': 'Link expired'}), 308  
    except ResponseError as e:
        jsonify({'message': str(e)}), e.status_code    


@main.route('/is_confirmed', methods=['POST'])
@login_required
def is_confirmed(user: UserDto):
    try:
        db = Database()
        value = db.get_confirmation_date(user.email) is not None
        return jsonify({'message': {'is_confirmed': value}}), 200
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code        


@main.route('/confirmation_date', methods=['POST'])
@login_required
def confirmation_date(user: UserDto):
    try:
        db = Database()
        value = db.get_confirmation_date(user.email)
        if value is None:
            raise DbError('User is not confirmed')
        return jsonify({'message': {'is_confirmed': value}}), 200
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code     

@main.route('/')
def index():
    return 'Welcome to the La-planta API!'

# TODO
@app.route("/map")
def api_map():
    pass
