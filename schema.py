from marshmallow import Schema, fields


class PersonSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PersonUpdateSchema(Schema):
    name = fields.Str()
