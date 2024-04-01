#!/usr/bin/python3
"""
Defines routes for handling Amenity objects and operations.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity

@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    Retrieves all Amenity objects.
    :return: JSON response containing all Amenity objects.
    """
    am_list = []
    am_obj = storage.all("Amenity")
    for obj in am_obj.values():
        am_list.append(obj.to_json())
    return jsonify(am_list)

@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    Creates a new Amenity object.
    :return: JSON response containing the newly created Amenity object.
    """
    am_json = request.get_json(silent=True)
    if am_json is None:
        abort(400, 'Not a JSON')
    if "name" not in am_json:
        abort(400, 'Missing name')
    new_am = Amenity(**am_json)
    new_am.save()
    resp = jsonify(new_am.to_json())
    resp.status_code = 201
    return resp

@app_views.route("/amenities/<amenity_id>",  methods=["GET"], strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Retrieves a specific Amenity object by ID.
    :param amenity_id: ID of the Amenity object to retrieve.
    :return: JSON response containing the Amenity object with the specified ID, or a 404 error if not found.
    """
    fetched_obj = storage.get("Amenity", str(amenity_id))
    if fetched_obj is None:
        abort(404)
    return jsonify(fetched_obj.to_json())

@app_views.route("/amenities/<amenity_id>",  methods=["PUT"], strict_slashes=False)
def amenity_put(amenity_id):
    """
    Updates a specific Amenity object by ID.
    :param amenity_id: ID of the Amenity object to update.
    :return: JSON response containing the updated Amenity object on success, or a 404 error if the object is not found.
    """
    am_json = request.get_json(silent=True)
    if am_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Amenity", str(amenity_id))
    if fetched_obj is None:
        abort(404)
    for key, val in am_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())

@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"], strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    Deletes an Amenity object by ID.
    :param amenity_id: ID of the Amenity object to delete.
    :return: Empty JSON response with status code 200 on success, or a 404 error if the object is not found.
    """
    fetched_obj = storage.get("Amenity", str(amenity_id))
    if fetched_obj is None:
        abort(404)
    storage.delete(fetched_obj)
    storage.save()
    return jsonify({})
