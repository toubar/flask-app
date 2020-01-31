from schema import Schema, SchemaMissingKeyError, SchemaError, SchemaWrongKeyError
from flask import jsonify, request
from functools import wraps
from services import app


class RequestValidator:
    schema = Schema({"service": str,
                     "ip": str,
                     "servers": [
                         {"name": str,
                          "status": str}
                     ]})

    @staticmethod
    def validate_request(f):
        # checks if request us a JSON
        @wraps(f)
        def decorator(*args, **kwargs):
            if request.json:
                app.logger.debug('Request is a valid JSON')
                return f(*args, **kwargs)
            else:
                msg = "payload must be a valid json"
                app.logger.error(msg)
                return jsonify(message=msg), 400

        return decorator

    @staticmethod
    def validate_schema(f):
        # checks if the request JSON complies with the Schema
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                RequestValidator.schema.validate(request.json)
                app.logger.debug("Request's JSON body complies with Schema")
            except (SchemaMissingKeyError, SchemaWrongKeyError, SchemaError) as e:
                app.logger.error(e.code)
                return jsonify(message=e.code), 400
            else:
                return f(*args, **kwargs)

        return wrapper
