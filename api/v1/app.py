#!/usr/bin/python3
"""Creating a Flask app"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask

app = Flask(__name__)
# Register app_views as a blueprint to the Flask Instance
app.register_blueprint(app_views)

# Declare a method to handle teardown of the app context


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

# Run the Flask server


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
