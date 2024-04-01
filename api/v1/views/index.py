#!/usr/bin/python3
"""
This module implements routes for retrieving the status and statistics of the application.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    Returns the status of the application.
    :return: JSON response containing the status "OK".
    """
    data = {
        "status": "OK"
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    Returns statistics of all objects in the application.
    :return: JSON response containing the count of each type of object (Amenity, City, Place, Review, State, User).
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp
