from zope.sqlalchemy import register
from sqlalchemy import engine_from_config
from sqlalchemy.orm import configure_mappers
from sqlalchemy.orm import sessionmaker

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from wim_web.database import models  # noqa

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_tm_session(session_factory, transaction_manager):
    db_session = session_factory()
    register(db_session, transaction_manager=transaction_manager)
    return db_session


def includeme(config):
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')
    # use pyramid_retry to retry a request when transient exceptions occur
    config.include('pyramid_retry')

    engine = engine_from_config(settings, 'sqlalchemy.')
    factory = sessionmaker()
    factory.configure(bind=engine)
    config.registry['db_session_factory'] = factory

    # make request.db_session available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        lambda r: get_tm_session(factory, r.tm),
        'db_session',
        reify=True
    )
