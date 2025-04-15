from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

def validate_data(data, schema):
    try:
        schema.load(data)
        return True
    except ValidationError as err:
        return {"error": err.messages}