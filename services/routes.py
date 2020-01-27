from flask import request, jsonify
from services import app, model
from services import threading

# todo - better name
services_data = model.Services()


# todo - move to model.py?
@app.before_request
def sync_with_db():
    if services_data.data == {} or services_data.is_data_updated:
        services_data.data = services_data.load_data_from_json()
        services_data.is_data_updated = False


@app.route('/services/', methods=['GET'])
def get_services():
    return jsonify(services_data.data), 200


@app.route('/services/', methods=['PUT'])
def put_service():
    request_json = request.json
    if validate_request_body(request_json):
        service_name = request_json['service']
        #  check if service exists or not
        if service_name in [service['service'] for service in services_data.data['services']]:
            services_data.update_service(request_json)  # service exists, update it
            threading.Compute(services_data.persist_data_in_db).start()  # respond to client then persist data in DB
            return 'Updated.', 200
        else:
            services_data.create_service(request_json)  # service name does not exists, create it
            threading.Compute(services_data.persist_data_in_db).start()  # respond to client then persist data in DB
            return 'Created.', 201
    else:
        return 'Incorrect request body.', 400


# todo - where should this validation be defined?
def validate_request_body(request_body):
    # todo - should redundant fields in the body invalidate the request?
    #  i.e. request body has ["ip", "servers", "service"] but also "locations"..
    if all(k in request_body.keys() for k in ["ip", "servers", "service"]):
        return True
    else:
        return False
