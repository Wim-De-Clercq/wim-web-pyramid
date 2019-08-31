from marshmallow import fields
from marshmallow import validate

from wim_web.schemas import WebSchema


class PaginationSchema(WebSchema):
    page = fields.Int(load_on=['GET'],
                      dump_onl=['GET'],
                      validate=validate.Range(min=1), missing=1)
    page_size = fields.Int(load_on=['GET'],
                           dump_onl=['GET'],
                           validate=validate.Range(min=1, max=100), missing=10)
