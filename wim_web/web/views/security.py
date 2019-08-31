from pyramid.httpexceptions import HTTPUnauthorized
from sqlalchemy.orm.exc import NoResultFound

from wim_web.database.models import User
from wim_web.schemas import auto_schema
from wim_web.schemas.user import LoginSchema
from wim_web.security import pw_hasher
from wim_web.web.views import View


class SecurityView(View):
    @auto_schema(body_schema=LoginSchema(request_method="POST"))
    def login(self):
        from sqlalchemy.orm.exc import MultipleResultsFound
        login_data = self.request.loaded['body']
        try:
            user = (
                self.db_session.query(User)
                .filter(User.email == login_data['email'])
            ).one()
        except (NoResultFound, MultipleResultsFound):
            raise HTTPUnauthorized

        # Verify password, raises exception if wrong.
        pw = login_data['password']
        pw_hasher.verify(user.pw_hash, pw)

        # when we update the hashing library, it may need updating.
        if pw_hasher.check_needs_rehash(user.pw_hash):
            user.pw_hash = pw_hasher.hash(pw)
        return user
