import typing

from pyramid.security import Allow
from pyramid.security import Authenticated

from wim_web.database.models import Item
from wim_web.database.models import User
from wim_web.exc import DatabaseResourceNotFound

if typing.TYPE_CHECKING:
    from typing import Optional
    from pyramid.request import Request


class Resource(object):
    __name__ = ''
    __parent__ = None

    def __init__(self, request: 'Request', key: 'Optional[str]') -> None:
        super().__init__()
        self.request = request
        self.key = key

    def __getitem__(self, key: 'str'):
        try:
            child_resource = next(resource.cls for resource in self.children
                                  if resource.regex.fullmatch(key))
        except StopIteration:
            raise KeyError

        resource = child_resource(self.request, key=key)
        resource.__parent__ = self
        resource.__name__ = key
        return resource

    @property
    def parent(self):
        return self.__parent__


class DatabaseResource(Resource):
    resource_name = 'resource'

    def __init__(self, model_class, request: 'Request', key: 'str') -> None:
        super().__init__(request, key)
        self.db_object = request.db_session.query(model_class).get(key)
        if self.db_object is None:
            msg = f"Could not find {self.resource_name} with key {key}"
            raise DatabaseResourceNotFound(msg)


class Root(Resource):
    def __init__(self, request: 'Request') -> None:
        super().__init__(request, None)


# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------
class UsersResource(Resource):
    __acl__ = [
        (Allow, 'admin', 'view-users'),
    ]


class RegisterResource(Resource):
    pass


class UserResource(DatabaseResource):
    resource_name = 'user'

    def __init__(self, request: 'Request', key: 'str') -> None:
        super().__init__(User, request, key)
        self.user = self.db_object

    @property
    def __acl__(self):
        if self.user.id == self.request.authenticated_userid:
            return [
                (Allow, self.request.authenticated_userid, 'view-user'),
                (Allow, self.request.authenticated_userid, 'edit-user'),
                (Allow, self.request.authenticated_userid, 'delete-user'),
            ]
        else:
            return [
                (Allow, 'admin', 'view-user'),
                (Allow, 'admin', 'edit-user'),
                (Allow, 'admin', 'delete-user'),
            ]


class UserEditResource(Resource):

    @property
    def user(self):
        return self.parent.user


# -----------------------------------------------------------------------------
# Items
# -----------------------------------------------------------------------------
class ItemResource(DatabaseResource):
    resource_name = 'item'
    __acl__ = [
        (Allow, Authenticated, 'view-item'),
        (Allow, Authenticated, 'edit-item'),
        (Allow, Authenticated, 'delete-item'),
    ]

    def __init__(self, request: 'Request', key: 'str') -> None:
        super().__init__(Item, request, key)
        self.item = self.db_object


class ItemEditResource(Resource):

    @property
    def item(self):
        return self.parent.item


class ItemCreateResource(Resource):
    pass


class ItemsResource(Resource):
    __acl__ = [
        (Allow, Authenticated, 'view-items'),
        (Allow, Authenticated, 'create-items'),
    ]
