from flask import Blueprint

root_blueprint = Blueprint('root', __name__)

API_VERSION = "1.0.0"
API_VERSION_PATH = f"/api/v{API_VERSION}"


@root_blueprint.route('/')
def root():
    # Return a JSON response indicating that the API is running, version, and status 200
    return {
        "message": "API is running",
        "version": API_VERSION,
        "status": 200
    }
