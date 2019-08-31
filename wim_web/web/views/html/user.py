from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNoContent
from pyramid.view import view_config

from wim_web import Root
from wim_web.schemas.user import UserSchema
from wim_web.web.resources import RegisterResource
from wim_web.web.resources import UserEditResource
from wim_web.web.resources import UsersResource
from wim_web.web.resources.tree import UserResource
from wim_web.web.views.html import HtmlView
from wim_web.web.views.html.forms.user import EditForm
from wim_web.web.views.html.forms.user import RegisterForm
from wim_web.web.views.user import UserView


class UserHtmlView(HtmlView, UserView):

    @view_config(context=UsersResource, request_method='GET',
                 renderer='users/list_users.mako', permission='view-users')
    def get_users(self):
        users = super().get_users()
        return {'users': users}

    @view_config(context=UserResource, request_method='GET',
                 renderer='users/show_user.mako', permission='view-user')
    def get_user(self):
        user = super().get_user()
        return {'user': user}

    @view_config(context=RegisterResource, request_method='GET',
                 renderer='users/create_user.mako')
    def get_register_page(self):
        form = RegisterForm()
        return {'form': form}

    @view_config(context=RegisterResource, request_method='POST',
                 renderer='users/create_user.mako')
    def create_user(self):
        try:
            user = super().create_user()
            self.add_success_notification(f'User {user.name} created.')
            return HTTPFound(
                location=self.request.resource_url(Root(self.request))
            )
        except ValidationError as e:
            form = RegisterForm(formdata=self.request.POST)
            form.password.value = None
            form.load_schema_errors(e.messages)
            return {'form': form}

    @view_config(context=UserEditResource, request_method='GET',
                 renderer='users/edit_user.mako', permission='edit-user')
    def get_edit_page(self):
        user = self.context.parent.user
        schema = UserSchema(request_method='PATCH')
        form = EditForm(data=schema.dump(user))
        return {'form': form,
                'user': user}

    @view_config(context=UserEditResource, request_method='POST',
                 renderer='users/edit_user.mako', permission='edit-user')
    def update_user(self):
        try:
            target = self.request.POST.pop('target')
            user = super().update_user()
            self.add_success_notification(f'User {user.name} edited.')
            if not target:
                target = self.request.resource_url(Root(self.request))
            return HTTPFound(location=target)
        except ValidationError as e:
            form = EditForm(formdata=self.request.POST)
            form.load_schema_errors(e.messages)
            return {'form': form,
                    'user': self.context.parent.user}

    @view_config(context=UserResource, request_method='DELETE',
                 permission='delete-user')
    def delete_user(self):
        user = super().delete_user()
        self.add_success_notification(f'User {user.name} deleted.')
        return HTTPNoContent()
