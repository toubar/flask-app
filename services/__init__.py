from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os



SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Services API"
    }
)

app = Flask(__name__, static_folder=os.path.abspath('static'))
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
CORS(app)

from services import routes