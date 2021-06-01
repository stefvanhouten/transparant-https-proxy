from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema

from api.models import Configurations


class GetConfigSchema(SQLAlchemySchema):
    ip = fields.IP(required=True)
    name = fields.Str(required=True)


class CreateConfigSchema(SQLAlchemySchema):
    class Meta:
        model = Configurations
        load_instance = True

    ip = fields.Str(required=True)
    name = fields.Str(required=True)
    block_iso = fields.Bool(required=True)
    exclude_elements = fields.List(fields.Str, required=True)
