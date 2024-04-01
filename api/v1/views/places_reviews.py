#!/usr/bin/python3
"""
Defines routes for handling Review objects and operations.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review

@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def reviews_by_place(place_id):
    """
    Retrieves all Review objects associated with a specific place.
    :param place_id: The ID of the place to retrieve reviews for.
    :return: JSON response containing all reviews associated with the specified place, or a 404 error if the place is not found.
    """
    review_list = []
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)
    for obj in place_obj.reviews:
        review_list.append(obj.to_json())
    return jsonify(review_list)

@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def review_create(place_id):
    """
    Creates a new Review object associated with a specific place.
    :param place_id: The ID of the place to associate the new review with.
    :return: JSON response containing the newly created Review object on success, or a 400 error if the request is not in JSON format, or a 404 error if the place or user referenced in the request does not exist, or a 400 error if required fields are missing.
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", review_json["user_id"]):
        abort(404)
    if "user_id" not in review_json:
        abort(400, 'Missing user_id')
    if "text" not in review_json:
        abort(400, 'Missing text')
    review_json["place_id"] = place_id
    new_review = Review(**review_json)
    new_review.save()
    resp = jsonify(new_review.to_json())
    resp.status_code = 201
    return resp

@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def review_by_id(review_id):
    """
    Retrieves a specific Review object by its ID.
    :param review_id: The ID of the review to retrieve.
    :return: JSON response containing the Review object with the specified ID on success, or a 404 error if the review is not found.
    """
    fetched_obj = storage.get("Review", str(review_id))
    if fetched_obj is None:
        abort(404)
    return jsonify(fetched_obj.to_json())

@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def review_put(review_id):
    """
    Updates a specific Review object by its ID.
    :param review_id: The ID of the review to update.
    :return: JSON response containing the updated Review object on success, or a 404 error if the review is not found, or a 400 error if the request is not in JSON format.
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Review", str(review_id))
    if fetched_obj is None:
        abort(404)
    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "place_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())

@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def review_delete_by_id(review_id):
    """
    Deletes a specific Review object by its ID.
    :param review_id: The ID of the review to delete.
    :return: Empty JSON response with status code 200 on success, or a 404 error if the review is not found.
    """
    fetched_obj = storage.get("Review", str(review_id))
    if fetched_obj is None:
        abort(404)
    storage.delete(fetched_obj)
    storage.save()
    return jsonify({})
