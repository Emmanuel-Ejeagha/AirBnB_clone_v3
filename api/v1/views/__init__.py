#!/usr/bin/python3
"""Creating a Flask app"""
from flask import Blueprint
from api.v1.views.index import *

# Create a Blueprint instance
app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")
