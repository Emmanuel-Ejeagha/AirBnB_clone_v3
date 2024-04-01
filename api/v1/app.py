#!/usr/bin/python3
"""
<<<<<<< HEAD
This script defines the main Flask application for the API.
=======
    This script starts a Flask web application
>>>>>>> 41123c1a6b5eef74a00a90ad9a52f81607b8067a
"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from flasgger import Swagger
from flasgger.utils import swag_from

# Initialize Flask application
app = Flask(__name__)
<<<<<<< HEAD

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register blueprints for API endpoints
=======
>>>>>>> 41123c1a6b5eef74a00a90ad9a52f81607b8067a
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

# Define teardown function to close the database connection after each request
@app.teardown_appcontext
<<<<<<< HEAD
def teardown(exception):
    """
    A function that is called when each request ends, closing the database connection.
    """
    storage.close()
=======
def teardown(self):
    """Removes the current SQLAlchemy Session"""
    return storage.close()
>>>>>>> 41123c1a6b5eef74a00a90ad9a52f81607b8067a

# Define error handler for 404 Not Found errors
@app.errorhandler(404)
<<<<<<< HEAD
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
=======
def error(e):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
>>>>>>> 41123c1a6b5eef74a00a90ad9a52f81607b8067a
