from pyramid.view import view_config
from pyramid.view import view_defaults

from wim_web import Root
from wim_web.web.views import View


@view_defaults(accept='text/html')
class HtmlView(View):

    def add_success_notification(self, message):
        self.request.session.flash(message, 'success-notifications')

    def add_failure_notification(self, message):
        self.request.session.flash(message, 'failure-notifications')


class HomeView(HtmlView):

    @view_config(context=Root, renderer='home.mako')
    def home(self):
        return {}
