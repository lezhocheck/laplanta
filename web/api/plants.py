from flask import Blueprint, request
from .auth import confirmation_required, Database
from .models import UserDto, PlantDto, PlantExtendedDto
from .utils import DbError, ResponseError
from .utils import exception_handler

plants = Blueprint('plants', __name__)


@plants.route('/plant', methods=['POST'])
@confirmation_required
@exception_handler
def add_plant(user: UserDto, **kwargs):
    plant = PlantDto(request.json, user)
    db = Database()
    id = db.add_plant(plant)
    return {'id': id}    


@plants.route('/plant/<plant_id>')
@confirmation_required
@exception_handler
def get_plant(user: UserDto, plant_id: int, **kwargs):
    try:
        db = Database()
        plant = db.get_plant(user, int(plant_id))
        return plant.convert_to_dict()
    except ValueError:
        raise DbError('Invalid plant id')   


@plants.route('/plant/<plant_id>', methods=['PUT'])
@confirmation_required
@exception_handler
def update_plant(user: UserDto, plant_id: int, **kwargs):
    try:
        if not len(request.json):
            raise ResponseError('Cannot update with empty params')
        plant = PlantExtendedDto(request.json, user, required=False)
        db = Database()
        db.update_plant(plant, int(plant_id))
    except ValueError:
        raise DbError('Invalid plant id') 


@plants.route('/plant/<plant_id>/', methods=['DELETE'])
@confirmation_required
@exception_handler
def delete_plant(user: UserDto, plant_id: int, **kwargs):
    try:
        db = Database()
        db.delete_plant(user, int(plant_id))
    except ValueError:
        raise DbError('Invalid plant id')


@plants.route('/plants')
@confirmation_required
@exception_handler
def get_plants(user: UserDto, **kwargs):
    db = Database()
    result = db.find_user(user, {'_id': 0, 'plants': 1})
    if not result:
        raise DbError('No plants')
    return result


# TODO
@plants.route('/plant/<plant_id>/status')
@confirmation_required
def get_plant_status(user: UserDto, plant_id: int, **kwargs):
    pass
