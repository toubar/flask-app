from flask import request, jsonify
from services import app
from services.model import ServicesModel
from services.schema_validator import SchemaValidator, validate_request, validate_schema

# todo - better name
services_data = ServicesModel()
#  todo - where to initialize?
json_validator = SchemaValidator()


# todo - move logic to model.py keep the function call
@app.before_request
def sync_with_db():
    if services_data.data == {} or services_data.is_data_updated:
        services_data.data = services_data.load_data_from_json()
        services_data.is_data_updated = False


@app.route('/services/', methods=['GET'])
def get_services():
    return jsonify(services_data.data), 200


@app.route('/services/', methods=['PUT'])
@validate_request
@validate_schema
def put_service():
    request_json = request.json
    service_name = request_json['service']
    #  check if service exists or not
    if service_name in [service['service'] for service in services_data.data['services']]:
        services_data.update_service(request_json)  # service exists, update it
        return 'Updated.', 200
    else:
        services_data.create_service(request_json)  # service name does not exists, create it
        return 'Created.', 201


@app.after_request
def sync_db(response):
    services_data.persist_data_in_db()
    return response
