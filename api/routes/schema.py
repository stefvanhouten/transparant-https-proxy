from marshmallow import Schema, ValidationError, validates_schema, fields

class GetConfigSchema(Schema):
  ip = fields.IP(required=True)

class CreateConfigSchema(Schema):
  ip = fields.IP(required=True)
  block_iso = fields.Bool(required=True)
  exclude_elements = fields.List(fields.Str, required=True)
