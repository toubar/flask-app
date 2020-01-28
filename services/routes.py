from flask import request, jsonify
from services import app
from services.model import ServicesModel
from services.schema_validator import SchemaValidator

# todo - better name
services_data = ServicesModel()


@app.before_request
def before_each_request():
    services_data.sync_data_with_db()


@app.route('/services/', methods=['GET'])
def get_services():
    return jsonify(services_data.data), 200


@app.route('/services/', methods=['PUT'])
@SchemaValidator.validate_request
@SchemaValidator.validate_schema
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
def after_each_request(response):
    services_data.persist_data_in_db()
    return response
