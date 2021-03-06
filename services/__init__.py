from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os
import logging
from flask_jwt_simple import JWTManager

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Services API"
    }
)

# logging configuration
logging.basicConfig(filename='logs.log', level=logging.INFO)

app = Flask(__name__, static_folder=os.path.abspath('static'))

# swagger UI registration
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# setting up Jason Web Tokens for endpoint protection
app.config['JWT_SECRET_KEY'] = 'confidential'
jwt = JWTManager(app)

# enabling Cross-Origin Resource Sharing (CORS)
CORS(app)

from services.model import ServicesModel

services_model = ServicesModel()

from services import routes
