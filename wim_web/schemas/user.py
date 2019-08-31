from marshmallow import fields

from wim_web.schemas import WebSchema
from wim_web.schemas import required
from wim_web.schemas.common import PaginationSchema


# Use 'attribute' kwarg when model field is not same as json field
class UserSchema(PaginationSchema):

    id = fields.Int(dump_on=['ALL'])
    name = fields.Str(load_on=['GET', 'POST', 'PATCH', 'POST'],
                      dump_on=['ALL'],
                      required_on=['POST'],
                      validate=[required])
    email = fields.Email(load_on=['GET', 'POST', 'PATCH', 'POST'],
                         dump_on=['ALL'],
                         required_on=['POST'],
                         validate=required)
    password = fields.Str(load_on=['POST'],
                          required_on=['POST'],
                          validate=required)


class LoginSchema(WebSchema):

    email = fields.Email(load_on=['POST'],
                         required_on=['POST'],
                         validate=[required])
    password = fields.Str(load_on=['POST'],
                          required_on=['POST'],
                          validate=[required])
