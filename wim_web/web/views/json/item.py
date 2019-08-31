from pyramid.httpexceptions import HTTPNoContent
from pyramid.view import view_config

from wim_web.schemas import auto_schema
from wim_web.schemas.item import ItemSchema
from wim_web.web.resources import ItemsResource
from wim_web.web.resources.tree import ItemResource
from wim_web.web.views.json import JsonView
from wim_web.web.views.item import ItemView


class ItemJsonView(JsonView, ItemView):

    @view_config(context=ItemsResource, request_method='GET')
    @auto_schema(response_schema=ItemSchema(many=True, request_method='GET'))
    def get_items(self):
        return super().get_items()

    @view_config(context=ItemResource, request_method='GET')
    @auto_schema(response_schema=ItemSchema(request_method='GET'))
    def get_item(self):
        return super().get_item()

    @view_config(context=ItemsResource, request_method='POST')
    @auto_schema(response_schema=ItemSchema(request_method='POST'))
    def create_item(self):
        return super().create_item()

    @view_config(context=ItemResource, request_method='PATCH')
    @auto_schema(response_schema=ItemSchema(request_method='PATCH'))
    def update_item(self):
        return super().update_item()

    @view_config(context=ItemResource, request_method='DELETE')
    def delete_item(self):
        super().delete_item()
        return HTTPNoContent()
