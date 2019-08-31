from wtforms import PasswordField

from wim_web.schemas.user import LoginSchema
from wim_web.schemas.user import UserSchema
from wim_web.web.views.html.forms import SchemaForm


class RegisterForm(SchemaForm):
    schema = UserSchema(request_method="POST")


class EditForm(SchemaForm):
    schema = UserSchema(request_method="PATCH")


class LoginForm(SchemaForm):
    schema = LoginSchema(request_method="POST")

    custom_fields = {
        'password': PasswordField
    }
