from flask import Flask
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
from flask_cors import CORS
import os
from flask_jwt_extended import JWTManager


def init_env(app: Flask):
    load_dotenv()
    variables = {
        'MONGO_DB_ADMIN_USER': str,
        'MONGO_DB_ADMIN_PASSWORD': str,

        'SECRET_KEY': str, 
        'PASSWORD_SALT': str, 
        
        'MAIL_SERVER': str, 
        'MAIL_PORT': int, 
        'MAIL_USERNAME': str, 
        'MAIL_PASSWORD': str,
        'MAIL_USE_TLS': bool, 
        'MAIL_USE_SSL': bool, 

        'UPLOAD_FOLDER': str
        }

    for var, var_type in variables.items():
        app.config[var] =  var_type(os.getenv(var))


app = Flask(__name__, static_folder='./static')
CORS(app, supports_credentials=True)
init_env(app)

app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
JWTManager(app)

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

from .main import main
app.register_blueprint(main)

from .auth import auth
app.register_blueprint(auth)

from .plants import plants
app.register_blueprint(plants)

from .sensors import sensors
app.register_blueprint(sensors)