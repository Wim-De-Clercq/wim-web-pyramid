from pyramid.httpexceptions import HTTPNoContent
from pyramid.view import view_config

from wim_web.schemas import auto_schema
from wim_web.schemas.user import UserSchema
from wim_web.web.resources import UsersResource
from wim_web.web.resources.tree import UserResource
from wim_web.web.views.json import JsonView
from wim_web.web.views.user import UserView


class UserJsonView(JsonView, UserView):

    @view_config(context=UsersResource, request_method='GET')
    @auto_schema(response_schema=UserSchema(many=True, request_method='GET'))
    def get_users(self):
        return super().get_users()

    @view_config(context=UserResource, request_method='GET')
    @auto_schema(response_schema=UserSchema(request_method='GET'))
    def get_user(self):
        return super().get_user()

    @view_config(context=UsersResource, request_method='POST')
    @auto_schema(response_schema=UserSchema(request_method='POST'))
    def create_user(self):
        return super().create_user()

    @view_config(context=UserResource, request_method='PATCH')
    @auto_schema(response_schema=UserSchema(request_method='PATCH'))
    def update_user(self):
        return super().update_user()

    @view_config(context=UserResource, request_method='DELETE')
    def delete_user(self):
        super().delete_user()
        return HTTPNoContent()
