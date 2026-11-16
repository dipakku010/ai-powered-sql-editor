"""Simple Flask Hello World API

Run with:
    python flask_app.py

Then visit http://127.0.0.1:5000/hello to see the response.
"""

from flask import Flask, jsonify

# Import the cache instance and SQL editor blueprint from the ai_sql_editor module.
from ai_sql_editor import cache, sql_editor_bp

# Initialize the Flask app and configure caching.
app = Flask(__name__)

# Configure caching for the Flask app using the cache instance from ai_sql_editor.
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 3600

# Initialize the cache with the Flask app.
cache.init_app(app)


# Define a simple hello world route for testing the Flask app.
@app.route("/hello", methods=["GET"])
def hello_world():
    """Return a friendly greeting as JSON."""
    return jsonify(message="Hello, World!")


# lets include the ai_sql_editor routes into this Flask app
app.register_blueprint(sql_editor_bp)


if __name__ == "__main__":
    # Enable debug mode for development; remove or set to False in production.
    app.run(host="0.0.0.0", port=5002, debug=True)
