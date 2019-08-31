from marshmallow import fields

from wim_web.schemas import required
from wim_web.schemas.common import PaginationSchema


# Use 'attribute' kwarg when model field is not same as json field
class ItemSchema(PaginationSchema):

    id = fields.Int(dump_on=['ALL'])
    user_id = fields.Int(dump_on=['ALL'])
    title = fields.Str(load_on=['GET', 'POST', 'PATCH', 'POST'],
                       dump_on=['ALL'],
                       required_on=['POST'],
                       validate=[required])
    description = fields.Str(load_on=['GET', 'POST', 'PATCH', 'POST'],
                             dump_on=['ALL'])
