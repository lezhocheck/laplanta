from flask import Blueprint, current_app, url_for, jsonify, request

from .models import UserDto, PlantDto
from .auth import login_required, Database
from api import serializer, app
from .utils import DbError, ResponseError


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Welcome to the La-planta API!'

# TODO
@app.route("/map")
def api_map():
    pass
