#!/usr/bin/python3
"""
Defines routes for handling User objects and their operations.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User

@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    Retrieves all User objects.
    :return: JSON response containing all users.
    """
    user_list = []
    user_obj = storage.all("User")
    for obj in user_obj.values():
        user_list.append(obj.to_json())
    return jsonify(user_list)

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    Creates a new User object.
    :return: JSON response containing the newly created User object on success, or a 400 error if the request is not in JSON format or if the 'email' or 'password' field is missing.
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')
    new_user = User(**user_json)
    new_user.save()
    resp = jsonify(new_user.to_json())
    resp.status_code = 201
    return resp

@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    Retrieves a specific User object by its ID.
    :param user_id: The ID of the user to retrieve.
    :return: JSON response containing the User object with the specified ID on success, or a 404 error if the user is not found.
    """
    fetched_obj = storage.get("User", str(user_id))
    if fetched_obj is None:
        abort(404)
    return jsonify(fetched_obj.to_json())

@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    Updates a specific User object by its ID.
    :param user_id: The ID of the user to update.
    :return: JSON response containing the updated User object on success, or a 404 error if the user is not found, or a 400 error if the request is not in JSON format.
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("User", str(user_id))
    if fetched_obj is None:
        abort(404)
    for key, val in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())

@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """
    Deletes a specific User object by its ID.
    :param user_id: The ID of the user to delete.
    :return: Empty JSON response with status code 200 on success, or a 404 error if the user is not found.
    """
    fetched_obj = storage.get("User", str(user_id))
    if fetched_obj is None:
        abort(404)
    storage.delete(fetched_obj)
    storage.save()
    return jsonify({})
