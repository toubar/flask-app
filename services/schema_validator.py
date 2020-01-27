from schema import Schema, SchemaMissingKeyError, SchemaError, SchemaWrongKeyError


class SchemaValidator:
    def __init__(self):
        self.schema = Schema({"service": str,
                              "ip": str,
                              "servers": [
                                  {"name": str,
                                   "status": str}
                              ]})

    def validate_json(self, json):
        try:
            self.schema.validate(json)
        except SchemaMissingKeyError as e:
            print(e.code)
            return {"valid": False, "message": e.code}
        except SchemaWrongKeyError as e:
            print(e.code)
            return {"valid": False, "message": e.code}
        except SchemaError as e:
            print(e.code)
            return {"valid": False, "message": e.code}
        else:
            return {"valid": False, "message": "Request JSON is Valid"}
