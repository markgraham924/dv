from flask import Flask
from flask_cors import CORS
from routes.headers import headers_bp
from cache import cache  # Import the cache instance

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'simple'  # Use 'redis' or 'memcached' for more robust caching
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds

cache.init_app(app)  # Initialize the cache with the Flask app

app.register_blueprint(headers_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
