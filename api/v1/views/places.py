#!/usr/bin/python3
"""
Defines routes for handling Place objects and operations.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place

@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def places_by_city(city_id):
    """
    Retrieves all Place objects associated with a specific city.
    :param city_id: The ID of the city to retrieve places for.
    :return: JSON response containing all places associated with the specified city, or a 404 error if the city is not found.
    """
    place_list = []
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)
    for obj in city_obj.places:
        place_list.append(obj.to_json())
    return jsonify(place_list)

@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def place_create(city_id):
    """
    Creates a new Place object associated with a specific city.
    :param city_id: The ID of the city to associate the new place with.
    :return: JSON response containing the newly created Place object on success, or a 400 error if the request is not in JSON format, or a 404 error if the user or city referenced in the request does not exist, or a 400 error if required fields are missing.
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", place_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in place_json:
        abort(400, 'Missing user_id')
    if "name" not in place_json:
        abort(400, 'Missing name')
    place_json["city_id"] = city_id
    new_place = Place(**place_json)
    new_place.save()
    resp = jsonify(new_place.to_json())
    resp.status_code = 201
    return resp

@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_by_id(place_id):
    """
    Retrieves a specific Place object by its ID.
    :param place_id: The ID of the place to retrieve.
    :return: JSON response containing the Place object with the specified ID on success, or a 404 error if the place is not found.
    """
    fetched_obj = storage.get("Place", str(place_id))
    if fetched_obj is None:
        abort(404)
    return jsonify(fetched_obj.to_json())

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def place_put(place_id):
    """
    Updates a specific Place object by its ID.
    :param place_id: The ID of the place to update.
    :return: JSON response containing the updated Place object on success, or a 404 error if the place is not found, or a 400 error if the request is not in JSON format.
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Place", str(place_id))
    if fetched_obj is None:
        abort(404)
    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())

@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def place_delete_by_id(place_id):
    """
    Deletes a specific Place object by its ID.
    :param place_id: The ID of the place to delete.
    :return: Empty JSON response with status code 200 on success, or a 404 error if the place is not found.
    """
    fetched_obj = storage.get("Place", str(place_id))
    if fetched_obj is None:
        abort(404)
    storage.delete(fetched_obj)
    storage.save()
    return jsonify({})
