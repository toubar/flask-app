from schema import Schema, SchemaMissingKeyError, SchemaError, SchemaWrongKeyError
from flask import jsonify, request
from functools import wraps


class RequestValidator:
    schema = Schema({"service": str,
                     "ip": str,
                     "servers": [
                         {"name": str,
                          "status": str}
                     ]})

    @staticmethod
    def validate_request(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if request.json:
                print("ok")
                return f(*args, **kwargs)
            else:
                msg = "payload must be a valid json"
                return jsonify({"error": msg}), 400

        return decorator

    @staticmethod
    def validate_schema(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                RequestValidator.schema.validate(request.json)
            except SchemaMissingKeyError as e:
                print(e.code)
                return e.code, 400
            except SchemaWrongKeyError as e:
                print(e.code)
                return e.code, 400
            except SchemaError as e:
                print(e.code)
                return e.code, 400
            else:
                return f(*args, **kwargs)

        return wrapper
