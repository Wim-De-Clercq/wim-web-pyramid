from wtforms import TextAreaField

from wim_web.schemas.item import ItemSchema
from wim_web.web.views.html.forms import SchemaForm


class CreateForm(SchemaForm):
    schema = ItemSchema(request_method="POST")
    custom_fields = {
        'description': TextAreaField
    }


class EditForm(SchemaForm):
    schema = ItemSchema(request_method="PATCH")
    custom_fields = {
        'description': TextAreaField
    }
