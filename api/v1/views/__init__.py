#!/usr/bin/python3
"""
This module defines a blueprint for routes using the Flask Blueprint object.
"""

from flask import Blueprint

# Create a Blueprint object for API version 1
app_views = Blueprint('api_v1', __name__, url_prefix="/api/v1")

# Import views for various endpoints
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.users import *
from api.v1.views.places_amenities import *
