import typing

if typing.TYPE_CHECKING:
    from pyramid.request import Request
    from sqlalchemy.orm import Session

    from wim_web.web.resources.tree import WebResource


class View(object):

    def __init__(self, context: 'WebResource', request: 'Request') -> None:
        super().__init__()
        self.context = context
        self.request = request
        self.db_session: 'Session' = request.db_session

    def load_page_db_params(self):
        params = self.request.loaded['querystring']
        page = params.pop('page')
        page_size = params.pop('page_size')
        return page_size * (page - 1), page_size
