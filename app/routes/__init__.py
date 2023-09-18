import os

from flask import Flask

from .loans import loans_blueprint
from .payments import payments_blueprint
from .root import root_blueprint
# Import the blueprints
from .users import users_blueprint

API_VERSION_PATH = os.getenv("API_VERSION_PATH", "/api/v1")


def register_routes(app: Flask):
    """Register the blueprints with the Flask app."""
    app.register_blueprint(users_blueprint, url_prefix=f'{API_VERSION_PATH}/data/users')
    app.register_blueprint(loans_blueprint, url_prefix=f'{API_VERSION_PATH}/data/loans')
    app.register_blueprint(payments_blueprint, url_prefix=f'{API_VERSION_PATH}/data/payments')
    app.register_blueprint(root_blueprint)
