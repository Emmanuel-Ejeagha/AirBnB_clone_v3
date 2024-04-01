#!/usr/bin/python3
"""
This script defines the main Flask application for the API.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register blueprints for API endpoints
app.register_blueprint(app_views)

# Define teardown function to close the database connection after each request
@app.teardown_appcontext
def teardown(exception):
    """
    A function that is called when each request ends, closing the database connection.
    """
    storage.close()

# Define error handler for 404 Not Found errors
@app.errorhandler(404)
def handle_404(exception):
    """
    A function to handle 404 Not Found errors, returning a JSON response.
    """
    data = {
        "error": "Not found"
    }
    resp = jsonify(data)
    resp.status_code = 404
    return resp

# Run the Flask application
if __name__ == "__main__":
    # Get API host and port from environment variables, defaulting to 0.0.0.0:5000
    host = getenv("HBNB_API_HOST") or "0.0.0.0"
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=port)
