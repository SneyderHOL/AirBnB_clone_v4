#!/usr/bin/python3
''' endpoints for json views '''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def views_json():
    """ Return Json """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_each_obj():
    '''
        Endpoint that retrieves the number
        of each objects by type:
    '''
    objs_size = {}
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    for cls_k, cls_v in classes.items():
        objs_size[cls_k] = storage.count(cls_v)
    return jsonify(objs_size)
