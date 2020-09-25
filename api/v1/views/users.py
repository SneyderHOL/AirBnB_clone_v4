#!/usr/bin/python3
''' endpoints for users views '''
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


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users_recovery():
    """
        Retrieves the list of all User objects:
        GET /api/v1/users

        Creates a User: POST /api/v1/users
            If the HTTP body request is not valid JSON,
            raise a 400 error with the message Not a JSON
            If the dictionary doesn’t contain the key email,
            raise a 400 error with the message Missing email
            If the dictionary doesn’t contain the key password,
            raise a 400 error with the message Missing password
            Returns the new User with the status code 201
    """
    if request.method == 'GET':
        all_users = storage.all(User)
        all_users_ls = []
        for usr_obj in all_users.values():
            all_users_ls.append(usr_obj.to_dict())
        return jsonify(all_users_ls)

    if request.method == 'POST':
        if not request.is_json:
            abort(400, description='Not a JSON')
        json_data = request.get_json()
        if 'email' not in json_data:
            abort(400, description='Missing email')
        if 'password' not in json_data:
            abort(400, description='Missing password')
        newUser = User(**json_data)
        storage.new(newUser)
        storage.save()
        return jsonify(newUser.to_dict()), 201
    abort(404)


@app_views.route('/users/<user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def users_by_id(user_id):
    '''
        Retrieves a User object: GET /api/v1/users/<user_id>
            If the user_id is not linked to any User object,
            raise a 404 error

        Deletes a User object:: DELETE /api/v1/users/<user_id>
            If the user_id is not linked to any User object,
            raise a 404 error
            Returns an empty dictionary with the status code 200

        Updates a User object: PUT /api/v1/users/<user_id>
            If the user_id is not linked to any User object,
            raise a 404 error
            If the HTTP body request is not valid JSON,
            raise a 400 error with the message Not a JSON
            Update the User object with all key-value
            pairs of the dictionary
            Ignore keys: id, email, created_at and updated_at
            Returns the User object with the status code 200
    '''
    usr_obj = storage.get(User, user_id)
    if usr_obj is not None:
        if request.method == 'GET':
            return jsonify(usr_obj.to_dict())

        if request.method == 'DELETE':
            storage.delete(usr_obj)
            storage.save()
            return jsonify({}), 200

        if request.method == 'PUT':
            json_data = request.get_json()
            catched = storage.get(User, user_id)
            if not request.is_json:
                abort(400, description='Not a JSON')
            if catched is not None:
                for k, v in json_data.items():
                    if k not in ['id', 'created_at', 'updated_at', 'email']:
                        setattr(catched, k, v)
                storage.save()
                return jsonify(catched.to_dict()), 200
    abort(404)
