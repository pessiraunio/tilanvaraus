from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema



class RoomSchema(Schema):
    class Meta:
        ordered = True
    

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(required=True, validate=[validate.Length(max=100)])
    location = fields.String(required=True, validate=[validate.Length(max=100)])
    is_listed = fields.Boolean(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data

    author = fields.Nested(UserSchema, attribute='user', dump_only=True,
                           only=['id', 'username'])
