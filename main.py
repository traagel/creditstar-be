import os

from flask import Flask
from flask_cors import CORS

from app.routes import register_routes
from app.services.database import Session
from app.services.database import create_db_engine

print(os.getcwd())
# Initialize the Flask app
app = Flask(__name__)
# Listen to 0.0.0.0 instead of localhost so that the app is accessible from outside the container


# CORS
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Load configurations (you can adjust this as needed, e.g., based on environment variables or other settings)
app.config.from_object("app.config.development")  # You can use app.config.production in a production environment

# Set up the database engine
engine = create_db_engine(app)

Session.configure(bind=engine)
# Register routes


register_routes(app)


# Teardown the session after each request to ensure it's closed and the connection is returned to the pool
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
