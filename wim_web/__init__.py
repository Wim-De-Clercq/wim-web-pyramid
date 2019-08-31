from pyramid import request
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.decorator import reify
from pyramid.session import SignedCookieSessionFactory

from wim_web.database.models import User
from wim_web.security import groupfinder
from wim_web.web.resources import Root
from wim_web.web.views.html.forms import initialize_forms


class Request(request.Request):

    def has_path_permission(self, permission, path):
        context = self.root
        for part in path.split('/'):
            if not part:
                continue
            try:
                context = context[part]
            except KeyError:
                break
        return self.has_permission(permission, context=context)

    @reify
    def user(self):
        if self.authenticated_userid:
            return self.db_session.query(User).get(self.authenticated_userid)
        else:
            return None


def main(global_config, **settings):
    with Configurator(settings=settings, root_factory=Root) as config:
        config.set_request_factory(Request)
        # mako
        registry_settings = config.registry.settings
        if 'mako.directories' not in registry_settings:
            registry_settings['mako.directories'] = 'wim_web:web/templates'
        # Configuration to show 'None' as empty string
        registry_settings['mako.imports'] = (
            'from markupsafe import escape_silent'
        )
        registry_settings['mako.default_filters'] = 'escape_silent'

        # session
        session_factory = SignedCookieSessionFactory(
            settings['wim_web.session_secret']
        )
        config.set_session_factory(session_factory)

        # auth
        authn_policy = AuthTktAuthenticationPolicy(
            settings['wim_web.secret'], callback=groupfinder,
            hashalg='sha512')
        authz_policy = ACLAuthorizationPolicy()
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)

        # includes
        config.include('pyramid_tm')
        config.include('wim_web.database')
        config.include('pyramid_mako')

        # frontend
        config.add_static_view('static', 'wim_web:web/static',
                               cache_max_age=3600)

        # backend
        config.scan('wim_web.web.views')
        initialize_forms()
    return config.make_wsgi_app()


if __name__ == '__main__':
    import sys
    from pyramid.paster import get_appsettings
    from waitress import serve

    settings = get_appsettings(sys.argv[1])
    serve(main(None, **settings), port=6543)
