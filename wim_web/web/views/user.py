from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from wim_web import security
from wim_web.database.models import User
from wim_web.schemas import auto_schema
from wim_web.schemas.user import UserSchema
from wim_web.web.views import View


class UserView(View):

    @auto_schema(querystring_schema=UserSchema(request_method='GET'))
    def get_users(self):
        offset, limit = self.load_page_db_params()
        params = self.request.loaded['querystring']
        return (
            self.db_session.query(User)
            .filter_by(**params)
            .offset(offset)
            .limit(limit)
            .all()
        )

    @auto_schema(querystring_schema=UserSchema(request_method='GET'))
    def get_user(self):
        return self.context.user

    @auto_schema(body_schema=UserSchema(request_method='POST'))
    def create_user(self):
        user_data = self.request.loaded['body']
        password = user_data.pop('password')
        user = User(**user_data)
        user.pw_hash = security.hash_password(password)
        try:
            self.db_session.add(user)
            self.db_session.flush()
        except IntegrityError:
            raise ValidationError({'email': ['Email already exists.']})
        return user

    @auto_schema(body_schema=UserSchema(request_method='PATCH'))
    def update_user(self):
        user_data = self.request.loaded['body']
        user = self.context.user
        for key, value in user_data.items():
            setattr(user, key, value)
        return user

    def delete_user(self):
        self.db_session.delete(self.context.user)
        return self.context.user
