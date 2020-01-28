from schema import Schema, SchemaMissingKeyError, SchemaError, SchemaWrongKeyError
from flask import jsonify, request


class SchemaValidator:
    def __init__(self):
        self.schema = Schema({"service": str,
                              "ip": str,
                              "servers": [
                                  {"name": str,
                                   "status": str}
                              ]})


# todo - how to structure the decorators
def validate_request(f):
    def wrapper(*args, **kw):
        if request.json:
            print("ok")
            return f(*args, **kw)
        else:
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400

    return wrapper


def validate_schema(f):
    def wrapper(*args, **kw):
        try:
            json_validator = SchemaValidator()
            json_validator.schema.validate(request.json)
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
            return f(*args, **kw)

    return wrapper
