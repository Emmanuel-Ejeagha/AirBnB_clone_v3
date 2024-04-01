#!/usr/bin/python3
"""
    This script starts a Flask web application for the AirBnB clone Restful API.
"""

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.register_blueprint(app_views)

# Enable CORS for all routes with a prefix of /api/v1/
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(self):
    """
    Removes the current SQLAlchemy Session at the end of the request.
    """
    return storage.close()

@app.errorhandler(404)
def error(e):
    """
    Handler for 404 errors, returns a JSON response with a 404 status code.
    """
    return jsonify({"error": "Not found"}), 404

# Configuration for Swagger UI
app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)

if __name__ == '__main__':
    # Retrieve host and port from environment variables or use default values
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    # Start the Flask web application
    app.run(host=host, port=port, threaded=True)
