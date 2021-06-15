from marshmallow import fields, post_load, pre_dump
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

    @pre_dump
    def pre_dump(self, data, **kwargs):
        if data is not None and data.exclude_elements:
            data.exclude_elements = [
                element for element in data.exclude_elements.split(",")
            ]
            return data

    @post_load
    def post_load(self, data, **kwargs):
        if data is not None and data.exclude_elements:
            data.exclude_elements = ",".join(data.exclude_elements)
            return data
