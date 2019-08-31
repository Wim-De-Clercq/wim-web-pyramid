from argon2.exceptions import VerifyMismatchError
from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.security import remember
from pyramid.view import view_config

from wim_web import Root
from wim_web.web.views.html import HtmlView
from wim_web.web.views.html.forms.user import LoginForm
from wim_web.web.views.security import SecurityView


class SecurityHtmlView(HtmlView, SecurityView):

    @view_config(context=Root, name='login', request_method='GET',
                 renderer='login.mako')
    def get_login_page(self):
        form = LoginForm()
        return {'form': form}

    @view_config(context=Root, name='login', request_method='POST',
                 renderer='login.mako')
    def login(self):
        try:
            user = super().login()
            headers = remember(self.request, user.id)
            target = self.request.params.get('target', '/')
            return HTTPFound(location=target, headers=headers)
        except ValidationError as e:
            form = LoginForm(self.request.POST)
            form.load_schema_errors(e.messages)
            return {'form': form}
        except VerifyMismatchError:
            form = LoginForm(self.request.POST)
            form.errors[''] = ['Incorrect login data.']
            return {'form': form}

    @view_config(context=Root, name='logout', request_method='GET')
    def logout(self):
        headers = forget(self.request)
        target = self.request.params.get('target', '/')
        return HTTPFound(location=target, headers=headers)
