#!/usr/bin/python3
""" Flask App runner """
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
# from api.v1.views import app_views
from os import getenv
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
PORT = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000
HOST = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else "0.0.0.0"
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(error):
    """ Handle Error """
    storage.close()


@app.errorhandler(404)
def error_404_not_found(self):
    ''' handle 404 erro '''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)
