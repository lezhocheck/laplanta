from flask import Blueprint, request, jsonify
from .auth import login_required, Database
from .models import UserDto, PlantDto, PlantExtendedDto
from .utils import DbError, ResponseError


plants = Blueprint('plants', __name__)


@plants.route('/plant/add', methods=['POST'])
@login_required
def add_plant(user: UserDto):
    try:
        plant = PlantDto(request.json, user)
        db = Database()
        id = db.add_plant(plant)
        return jsonify({'message': {'result': 'You successfuly added a plant', 'id': id}}), 200 
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code      


@plants.route('/plant/<plant_id>')
@login_required
def get_plant(user: UserDto, plant_id: int):
    try:
        db = Database()
        plant = db.get_plant(user, int(plant_id))
        return jsonify({'message': plant.convert_to_dict()}), 200
    except ValueError:
        return jsonify({'message': 'Invalid plant id'}), 402        
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code     


@plants.route('/plant/<plant_id>/update', methods=['POST'])
@login_required
def update_plant(user: UserDto, plant_id: int):
    try:
        if not len(request.json):
            raise ResponseError('Cannot update with empty params')
        plant = PlantExtendedDto(request.json, user, required=False)
        db = Database()
        db.update_plant(plant, int(plant_id))
        return jsonify({'message': 'The update was successful'}), 200
    except ValueError:
        return jsonify({'message': 'Invalid plant id'}), 402    
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code     


@plants.route('/plant/<plant_id>/delete')
@login_required
def delete_plant(user: UserDto, plant_id: int):
    try:
        db = Database()
        db.delete_plant(user, int(plant_id))
        return jsonify({'message': 'The deletion was successful'}), 200
    except ValueError:
        return jsonify({'message': 'Invalid plant id'}), 402    
    except ResponseError as e:
        return jsonify({'message': str(e)}), e.status_code  


@plants.route('/plant/all')
@login_required
def get_plants(user: UserDto):
    pass


@plants.route('/plant<plant_id>/estimate')
@login_required
def get_plant_estimation(user: UserDto, plant_id: int):
    pass


@plants.route('/plant<plant_id>/sensor/add', methods=['POST'])
@login_required
def add_sensor_record(user: UserDto, plant_id: int):
    db = Database()
    users = db.get_db()
    users

@plants.route('/sensors/get<plant_id>', methods=['POST'])
@login_required
def get_sensor_records(user: UserDto, plant_id: int):
    db = Database()
    users =  db.get_db()
    plant = users.find_one({'email': user.email, 'plants._id': plant_id}, {'_id': 0, 'plants': 1})
    if not plant:
        raise DbError('Plant do not exist')
    return jsonify({'message': plant['sensors']}), 200    