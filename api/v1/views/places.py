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


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_of_cities(city_id):
    '''
        Retrieves the list of all Place objects of a City:
            GET /api/v1/cities/<city_id>/places
            If the city_id is not linked to any City object,
            raise a 404 error

        Creates a Place:
            POST /api/v1/cities/<city_id>/places
            If the city_id is not linked to any City object,
            raise a 404 error
            If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            If the dictionary doesn’t contain the key user_id,
            raise a 400 error with the message Missing user_id
            If the user_id is not linked to any User object,
            raise a 404 error
            If the dictionary doesn’t contain the key name,
            raise a 400 error with the message Missing name
            Returns the new Place with the status code 201
    '''
    city_obj = storage.get(City, city_id)
    if city_obj is not None:
        if request.method == 'GET':
            places = storage.all(Place)
            places_list = []
            for place in places.values():
                if place.city_id == city_id:
                    places_list.append(place.to_dict())
            return jsonify(places_list)

        if request.method == 'POST':
            json_data = request.get_json()
            if not request.is_json:
                abort(400, description='Not a JSON')
            if 'user_id' not in json_data:
                abort(400, description='Missing user_id')
            if 'name' not in json_data:
                abort(400, description='Missing name')
            if storage.get(User, json_data['user_id']) is not None:
                newPlace = Place(**json_data)
                newPlace.city_id = city_id
                storage.new(newPlace)
                storage.save()
                return jsonify(newPlace.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_places_by_id(place_id):
    '''
        Retrieves a Place object. :
            GET /api/v1/places/<place_id>
            If the place_id is not linked to any Place object,
            raise a 404 error

        Deletes a Place object:
            DELETE /api/v1/places/<place_id>
            If the place_id is not linked to any Place object,
            raise a 404 error
            Returns an empty dictionary with the status code 200

        Updates a Place object:
            PUT /api/v1/places/<place_id>
            If the place_id is not linked to any Place object,
            raise a 404 error
            If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            Update the Place object with all key-value
            pairs of the dictionary
            Ignore keys: id, user_id, city_id, created_at and updated_at
            Returns the Place object with the status code 200
    '''
    place_obj = storage.get(Place, place_id)
    if place_obj is not None:
        if request.method == 'GET':
            return jsonify(place_obj.to_dict()), 200

        if request.method == 'DELETE':
            storage.delete(place_obj)
            storage.save()
            return jsonify({}), 200

        if request.method == 'PUT':
            json_data = request.get_json()
            if not request.is_json:
                abort(400, description='Not a JSON')
            for k, v in json_data.items():
                if k not in ['id',
                             'user_id',
                             'city_id',
                             'created_at',
                             'updated_at']:
                    setattr(place_obj, k, v)
            storage.save()
            return jsonify(place_obj.to_dict()), 200
    abort(404)

@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
# @swag_from('swagger_spec/search_places.yml')
def search_places():
    """Searches Places to data"""
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if len(data) == 0:
        list_places = [place.to_dict()
                       for place in storage.all(Place).values()]
        return jsonify(list_places)
    len_states = len(data['states']) if 'states' in data else 0
    len_cities = len(data['cities']) if 'cities' in data else 0
    len_amenities = len(data['amenities']) if 'amenities' in data else 0
    if len_states == 0 and len_cities == 0 and len_amenities == 0:
        list_places = [place.to_dict()
                       for place in storage.all(Place).values()]
        return jsonify(list_places)
    list_states = []
    list_cities = []
    if len_states > 0:
        for state_id in data['states']:
            list_states.append(get_object(State, state_id))
        for state in list_states:
            for city in state.cities:
                list_cities.append(city)
    if len_cities > 0:
        for city_id in data['cities']:
            list_cities.append(get_object(City, city_id))
    list_cities = list(set(list_cities))
    list_places = []
    for city in list_cities:
        for place in city.places:
            list_places.append(place)
    if len_states == 0 and len_cities == 0:
        list_places = storage.all(Place).values()
    if (len_states > 0 or len_cities > 0) and len(list_places) == 0:
        return jsonify({})
    if len_amenities == 0:
        result = [place.to_dict() for place in list_places]
        return jsonify(result)
    places_in_search = []

    for place in list_places:
        checked = True
        if environ.get('HBNB_TYPE_STORAGE') == 'db':
            place_amenities = [amenity.id for amenity in place.amenities]
        else:
            place_amenities = place.amenity_ids
        for amenity_id in data['amenities']:
            if amenity_id not in place_amenities:
                checked = False
                break
        if checked is True:
            del(place.amenities)
            places_in_search.append(get_object(Place, place.id))
    result = [place.to_dict() for place in places_in_search]
    return jsonify(result)


def get_object(cls, obj_id):
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj
