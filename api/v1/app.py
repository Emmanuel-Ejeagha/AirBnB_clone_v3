#!/usr/bin/python3
"""Creating a Flask app"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasger.utils import swang_from


app = Flask(__name__)
# Register app_views as a blueprint to the Flask Instance
app.register_blueprint(app_views)
cors = CORS(app, resourses={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Removes the current SQLAlchemy Session"""
    return storage.close()


@app.errorhandler(404)
def error(e):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


app.config['SWAGGER'] = {
    'title': 'AirBnB clone RESTful API',
    'uiversion': 3
}

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
