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


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def cities_by_state(state_id):
    '''
        Retrieves the list of all City objects of a State:
        GET /api/v1/states/<state_id>/cities

        If the state_id is not linked to any State object
        raise a 404 error

        Creates a City: POST /api/v1/states/<state_id>/cities
        If the state_id is not linked to any State object, raise a 404 error
        If the HTTP body request is not a valid JSON, raise a 400 error with
        the message Not a JSON
        If the dictionary doesn’t contain the key name, raise a 400 error with
        the message Missing name
        Returns the new City with the status code 201
    '''
    state_obj = storage.get(State, state_id)
    if request.method == 'GET':
        if state_obj is not None:
            cities = storage.all(City)
            cities_list = []
            for city in cities.values():
                if city.state_id == state_id:
                    cities_list.append(city.to_dict())
            return jsonify(cities_list)

    if request.method == 'POST':
        json_data = request.get_json()
        if not request.is_json:
            abort(400, description='Not a JSON')
        if 'name' not in json_data:
            abort(400, description='Missing name')
        if state_obj is not None:
            newCity = City(**json_data)
            newCity.state_id = state_id
            storage.new(newCity)
            storage.save()
            return jsonify(newCity.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_city_by_id(city_id):
    '''
        Retrieves a City object. : GET /api/v1/cities/<city_id>
            If the city_id is not linked to any City object, raise a 404 error

        Deletes a City object: DELETE /api/v1/cities/<city_id>
            If the city_id is not linked to any City object, raise a 404 error
            Returns an empty dictionary with the status code 200

        Updates a City object: PUT /api/v1/cities/<city_id>
            If the city_id is not linked to any City object, raise a 404 error
            You must use request.get_json from Flask to transform the HTTP body
            request to a dictionary
            If the HTTP request body is not valid JSON, raise a 400 error with
            the message Not a JSON
            Update the City object with all key-value pairs of the dictionary
            Ignore keys: id, state_id, created_at and updated_at
            Returns the City object with the status code 200
    '''
    city_obj = storage.get(City, city_id)
    if city_obj is not None:
        if request.method == 'GET':
            return jsonify(city_obj.to_dict()), 200

        if request.method == 'DELETE':
            storage.delete(city_obj)
            storage.save()
            return jsonify({}), 200

        if request.method == 'PUT':
            json_data = request.get_json()
            if not request.is_json:
                abort(400, description='Not a JSON')
            for k, v in json_data.items():
                if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                    setattr(city_obj, k, v)
            storage.save()
            return jsonify(city_obj.to_dict()), 200
    abort(404)
