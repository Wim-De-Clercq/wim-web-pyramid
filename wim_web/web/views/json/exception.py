from marshmallow import ValidationError
from pyramid.view import exception_view_config

from wim_web.web.views.json import JsonView


class ExceptionJsonView(JsonView):
    @exception_view_config(ValidationError)
    def failed_validation(self):
        self.request.response.status_int = 400
        return self.context.messages
