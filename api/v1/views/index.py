#!/usr/bin/python3
"""Creating a Flask app"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

# Defines route /status


@app_views.route('/status', methods=['GET'])
def status():
    """ status route"""
    data = {
        "status": "OK"
    }
    response = jsonify(data)
    response.status_code = 200
    return response


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """an endpoint that retrieves the number of each objects by type"""

dict = {
    "amenities": storage.count("Amenity"),
    "cities": storage.count("City"),
    "places": storage.count("Places"),
    "reviews": storage.count("Review"),
    "states": storage.count("State"),
    "users": storage.count("User"),
}
    response = jsonify(dict)
    response.status_code = 200
    return response
