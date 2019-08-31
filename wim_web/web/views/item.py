from wim_web.database.models import Item
from wim_web.schemas import auto_schema
from wim_web.schemas.item import ItemSchema
from wim_web.web.views import View


class ItemView(View):

    @auto_schema(querystring_schema=ItemSchema(request_method='GET'))
    def get_items(self):
        offset, limit = self.load_page_db_params()
        params = self.request.loaded['querystring']
        return (
            self.db_session.query(Item)
            .filter_by(**params)
            .offset(offset)
            .limit(limit)
            .all()
        )

    @auto_schema(querystring_schema=ItemSchema(request_method='GET'))
    def get_item(self):
        return self.context.item

    @auto_schema(body_schema=ItemSchema(request_method='POST'))
    def create_item(self):
        item_data = self.request.loaded['body']
        item = Item(**item_data)
        item.user_id = self.request.authenticated_userid
        self.db_session.add(item)
        self.db_session.flush()
        return item

    @auto_schema(body_schema=ItemSchema(request_method='PATCH'))
    def update_item(self):
        item_data = self.request.loaded['body']
        item = self.context.item
        for key, value in item_data.items():
            setattr(item, key, value)
        return item

    def delete_item(self):
        self.db_session.delete(self.context.item)
        return self.context.item
