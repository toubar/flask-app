from flask import request, jsonify
from flask_jwt_simple import create_jwt, jwt_required
from services import app, services_model
from services.request_validator import RequestValidator


@app.before_request
def before_each_request():
    services_model.sync_data_with_db()


@app.route('/services', methods=['GET'])
def get_services():
    return jsonify(services_model.data), 200


@app.route('/services', methods=['PUT'])
@RequestValidator.validate_request
@RequestValidator.validate_schema
@jwt_required
def put_service():
    request_json = request.json
    service_name = request_json['service']
    #  check if service exists in DB or not
    if service_name in [service['service'] for service in services_model.data['services']]:
        services_model.update_service(request_json)  # service exists, update it
        return jsonify(message="Service Updated"), 200
    else:
        services_model.create_service(request_json)  # service name does not exists, create it
        return jsonify(message="Service Created"), 201


@app.route('/authenticate', methods=['POST'])
@RequestValidator.validate_request
def authenticate():
    request_json = request.get_json()
    # for a real app, real auth (username + password) will be used. This is just a PoC
    jwt_secret = request_json.get('jwt_secret', None)
    if not jwt_secret:
        return jsonify(message="Missing jwt_secret parameter"), 400

    if jwt_secret != "jwt_secret":
        return jsonify(message="Bad jwt_secret"), 401

    token = {'jwt': create_jwt(identity=jwt_secret)}
    return jsonify(token), 200


@app.after_request
def after_each_request(response):
    services_model.persist_data_in_db()
    return response
