from argon2 import PasswordHasher
from sqlalchemy.orm.exc import NoResultFound

from wim_web.database.models import User

pw_hasher = PasswordHasher()


def hash_password(pw):
    return pw_hasher.hash(pw)


def check_password(pw_hash, pw):
    return pw_hasher.verify(pw_hash, pw)


def groupfinder(user_id, request):
    """
    The first parameter is the one remembered via pyramid.security.remember
    """
    try:
        user = (
            request.db_session.query(User)
            .filter(User.id == user_id)
        ).one()
        return ['admin'] if user.admin else []
    except NoResultFound:
        pass
    return []
