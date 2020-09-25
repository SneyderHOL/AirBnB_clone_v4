#!/usr/bin/python3
''' endpoints for states views '''
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states_recovery():
    """ Retrieves the list of all State objects: GET """
    if request.method == 'GET':
        all_st = storage.all(State)
        all_st_ls = []
        for state_obj in all_st.values():
            all_st_ls.append(state_obj.to_dict())
        return jsonify(all_st_ls)
    if request.method == 'POST':
        if not request.is_json:
            abort(400, description='Not a JSON')
        json_data = request.get_json()
        if 'name' not in json_data:
            abort(400, description='Missing name')
        newState = State(**json_data)
        storage.new(newState)
        storage.save()
        return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def count_each_state(state_id):
    '''
        Retrieves a State object: GET /api/v1/states/<state_id>
    '''
    s_obj = storage.get(State, state_id)
    if s_obj is not None:
        if request.method == 'GET':
            return jsonify(s_obj.to_dict())

        if request.method == 'DELETE':
            storage.delete(s_obj)
            storage.save()
            return jsonify({}), 200

        if request.method == 'PUT':
            json_data = request.get_json()
            catched = storage.get(State, state_id)
            if not request.is_json:
                abort(400, description='Not a JSON')
            if catched is not None:
                for k, v in json_data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(catched, k, v)
                storage.save()
                return jsonify(catched.to_dict()), 200
    abort(404)
