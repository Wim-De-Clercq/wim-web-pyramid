from pyramid.view import view_config

from wim_web import Root
from wim_web.web.views.json import JsonView
from wim_web.web.views.security import SecurityView


class SecurityJsonView(JsonView, SecurityView):
    @view_config(context=Root, name='login', request_method='POST')
    def login(self):
        user = super().login()
        # jwt token?
        return {}
