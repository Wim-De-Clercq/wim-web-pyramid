import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.view import exception_view_config
from pyramid.view import forbidden_view_config
from pyramid.view import notfound_view_config

from wim_web import Root
from wim_web.exc import DatabaseResourceNotFound
from wim_web.web.views.html import HtmlView

LOG = logging.getLogger(__name__)


class ExceptionHtmlView(HtmlView):
    @exception_view_config(Exception, renderer='home.mako')
    def exception_view(self):
        LOG.exception('an error happened')
        try:
            msg = self.request.exception.message
        except AttributeError:
            msg = "An unexpected exception occurred."
        self.add_failure_notification(str(msg))
        return {}

    @forbidden_view_config()
    def forbidden(self):
        self.add_failure_notification("You are not allowed to do this.")
        return HTTPFound(
            location=self.request.resource_url(Root(self.request)) + 'login'
        )

    @notfound_view_config(renderer='404.mako')
    def notfound(self):
        msg = f"The page at '{self.request.exception.message}' does not exist."
        return {
            'msg': msg
        }

    @exception_view_config(DatabaseResourceNotFound, renderer='404.mako')
    def exception_view(self):
        LOG.exception(f'Could not find resource at {self.request.path}')
        try:
            msg = self.request.exception.message
        except AttributeError:
            msg = "Could not find resource."
        self.request.response.status_int = 404
        return {
            'msg': msg
        }
