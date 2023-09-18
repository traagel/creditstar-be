import os

# Determine the application's environment based on an environment variable
ENV_TYPE = os.environ.get('FLASK_ENV', 'development')

if ENV_TYPE == 'development':
    from .development import *
elif ENV_TYPE == 'production':
    from .production import *
elif ENV_TYPE == 'testing':
    from .testing import *
else:
    raise ValueError(f"Unknown FLASK_ENV value: {ENV_TYPE}. Expected 'development', 'production', or 'testing'.")
