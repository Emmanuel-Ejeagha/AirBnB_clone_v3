#!/usr/bin/python3
"""Creating a Flask app"""
from flask import Blueprint

# Create a Blueprint instance
app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
