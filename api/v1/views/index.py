#!/usr/bin/python3
"""This module implement arule that returns status of the application"""

from api.v1.views import app_views
from flask import jsonify
import models
from models.amentiy import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Defines route /status
@app_views.route('/status', methods=strict_slashes=False)
def view_status():
    """View function that returns a json message"""
    return jsonsify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
"""an endpoint that retrieves the number of each objects by type"""
def view_stats():
    """View function that retrives the number of each object by type"""
    return jsonify({
        "amenities": models.storage.count(Amenity),
        "cities": models.storage.count(City),
        "places": models.storage.count(Places),
        "reviews": models.storage.count(Review),
        "states": models.storage.count(State),
        "users": models.storage.count(User)
    })
