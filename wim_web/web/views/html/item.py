from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNoContent
from pyramid.view import view_config

from wim_web import Root
from wim_web.schemas.item import ItemSchema
from wim_web.web.resources import ItemCreateResource
from wim_web.web.resources import ItemEditResource
from wim_web.web.resources import ItemsResource
from wim_web.web.resources.tree import ItemResource
from wim_web.web.views.html import HtmlView
from wim_web.web.views.html.forms.item import CreateForm
from wim_web.web.views.html.forms.item import EditForm
from wim_web.web.views.item import ItemView


class ItemHtmlView(HtmlView, ItemView):

    @view_config(context=ItemsResource, request_method='GET',
                 renderer='items/list_items.mako', permission='view-items')
    def get_items(self):
        items = super().get_items()
        return {'items': items}

    @view_config(context=ItemResource, request_method='GET',
                 renderer='items/show_item.mako', permission='view-item')
    def get_item(self):
        item = super().get_item()
        return {'item': item}

    @view_config(context=ItemCreateResource, request_method='GET',
                 renderer='items/create_item.mako')
    def get_create_page(self):
        form = CreateForm()
        return {'form': form}

    @view_config(context=ItemCreateResource, request_method='POST',
                 renderer='items/create_item.mako')
    def create_item(self):
        try:
            target = self.request.POST.pop('target')
            item = super().create_item()
            self.add_success_notification(f'Item {item.title} created.')
            if not target:
                target = self.request.resource_url(Root(self.request))
            return HTTPFound(location=target)
        except ValidationError as e:
            form = CreateForm(formdata=self.request.POST)
            form.password.value = None
            form.load_schema_errors(e.messages)
            return {'form': form}

    @view_config(context=ItemEditResource, request_method='GET',
                 renderer='items/edit_item.mako', permission='edit-item')
    def get_edit_page(self):
        item = self.context.parent.item
        schema = ItemSchema(request_method='PATCH')
        form = EditForm(data=schema.dump(item))
        return {'form': form,
                'item': item}

    @view_config(context=ItemEditResource, request_method='POST',
                 renderer='items/edit_item.mako', permission='edit-item')
    def update_item(self):
        try:
            target = self.request.POST.pop('target')
            item = super().update_item()
            self.add_success_notification(f'Item {item.title} edited.')
            if not target:
                target = self.request.resource_url(Root(self.request))
            return HTTPFound(location=target)
        except ValidationError as e:
            form = EditForm(formdata=self.request.POST)
            form.load_schema_errors(e.messages)
            return {'form': form,
                    'item': self.context.parent.item}

    @view_config(context=ItemResource, request_method='DELETE',
                 permission='delete-item')
    def delete_item(self):
        item = super().delete_item()
        self.add_success_notification(f'Item {item.title} deleted.')
        return HTTPNoContent()
