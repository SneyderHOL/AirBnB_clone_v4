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


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def reviews_of_cities(place_id):
    '''
        Retrieves the list of all Review objects of a Place:
            GET /api/v1/places/<place_id>/reviews
            - If the place_id is not linked to any Place object,
            raise a 404 error

        Creates a Review:
            POST /api/v1/places/<place_id>/reviews
            - If the place_id is not linked to any Place object,
            raise a 404 error
            - If the HTTP body request is not valid JSON,
            raise a 400 error with the message Not a JSON
            - If the dictionary doesn’t contain the key user_id,
            raise a 400 error with the message Missing user_id
            - If the user_id is not linked to any User object,
            raise a 404 error
            - If the dictionary doesn’t contain the key text,
            raise a 400 error with the message Missing text
            Returns the new Review with the status code 201
    '''
    place_obj = storage.get(Place, place_id)
    if place_obj is not None:
        if request.method == 'GET':
            reviews = storage.all(Review)
            reviews_list = []
            for rvw in reviews.values():
                if rvw.place_id == place_id:
                    reviews_list.append(rvw.to_dict())
            return jsonify(reviews_list), 200

        if request.method == 'POST':
            json_data = request.get_json()
            if not request.is_json:
                abort(400, description='Not a JSON')
            if 'user_id' not in json_data:
                abort(400, description='Missing user_id')
            if 'text' not in json_data:
                abort(400, description='Missing text')
            if storage.get(User, json_data['user_id']) is not None:
                newReview = Review(**json_data)
                newReview.place_id = place_id
                storage.new(newReview)
                storage.save()
                return jsonify(newReview.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_reviews_by_id(review_id):
    '''
        Retrieves a Review object. :
            GET /api/v1/reviews/<review_id>
            - If the review_id is not linked to any Review object,
            raise a 404 error

        Deletes a Review object:
            DELETE /api/v1/reviews/<review_id>
            - If the review_id is not linked to any Review object,
            raise a 404 error
            Returns an empty dictionary with the status code 200

        Updates a Review object:
            PUT /api/v1/reviews/<review_id>
            - If the review_id is not linked to any Review object,
            raise a 404 error
            - If the HTTP request body is not valid JSON,
            raise a 400 error with the message Not a JSON
            Update the Review object with all key-value
            pairs of the dictionary
            Ignore keys: id, user_id, place_id, created_at and updated_at
            Returns the Review object with the status code 200
    '''
    review_obj = storage.get(Review, review_id)
    if review_obj is not None:
        if request.method == 'GET':
            return jsonify(review_obj.to_dict()), 200

        if request.method == 'DELETE':
            storage.delete(review_obj)
            storage.save()
            return jsonify({}), 200

        if request.method == 'PUT':
            json_data = request.get_json()
            if not request.is_json:
                abort(400, description='Not a JSON')
            for k, v in json_data.items():
                if k not in ['id',
                             'user_id',
                             'place_id',
                             'created_at',
                             'updated_at']:
                    setattr(review_obj, k, v)
            storage.save()
            return jsonify(review_obj.to_dict()), 200
    abort(404)
