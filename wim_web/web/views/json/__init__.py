from pyramid.view import view_defaults

from wim_web.web.views import View


@view_defaults(accept='application/json', renderer='json')
class JsonView(View):
    pass
