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


@app_views.route('/amenities',
                 methods=['GET', 'POST'], strict_slashes=False)
def all_amenities():
    '''
        Retrieves the list of all Amenity objects:
        GET /api/v1/amenities

        Creates a Amenity: POST /api/v1/amenities
            If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON

            If the dictionary doesn’t contain the key name,
            raise a 400 error with the message Missing name
            Returns the new Amenity with the status code 201
    '''
    amenity_objs = storage.all(Amenity)
    if amenity_objs is not None:
        if request.method == 'GET':
            amenities_list = []
            for amenity in amenity_objs.values():
                amenities_list.append(amenity.to_dict())
            return jsonify(amenities_list)

        if request.method == 'POST':
            json_data = request.get_json()
            if not request.is_json:
                abort(400, description='Not a JSON')
            if 'name' not in json_data:
                abort(400, description='Missing name')
            newAmenity = Amenity(**json_data)
            storage.new(newAmenity)
            storage.save()
            return jsonify(newAmenity.to_dict()), 201
    abort(404)


@app_views.route('amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_amenity_id(amenity_id):
    '''
        Retrieves a Amenity object:
            GET /api/v1/amenities/<amenity_id>
            If the amenity_id is not linked to any Amenity object,
            raise a 404 error

        Deletes a Amenity object:
            DELETE /api/v1/amenities/<amenity_id>
            If the amenity_id is not linked to any Amenity object,
            raise a 404 error
            Returns an empty dictionary with the status code 200

        Updates a Amenity object:
            PUT /api/v1/amenities/<amenity_id>
            If the amenity_id is not linked to any Amenity object,
            raise a 404 error
            If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            Update the Amenity object with all key-value
            pairs of the dictionary
            Ignore keys: id, created_at and updated_at
            Returns the Amenity object with the status code 200
    '''
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is not None:
        if request.method == 'GET':
            return jsonify(amenity_obj.to_dict())

        if request.method == 'DELETE':
            storage.delete(amenity_obj)
            storage.save()
            return jsonify({}), 200

        if request.method == 'PUT':
            json_data = request.get_json()
            fetch_amenity = storage.get(Amenity, amenity_id)
            if not request.is_json:
                abort(400, description='Not a JSON')
            if fetch_amenity is not None:
                for k, v in json_data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(fetch_amenity, k, v)
                storage.save()
                return jsonify(fetch_amenity.to_dict()), 200
    abort(404)
