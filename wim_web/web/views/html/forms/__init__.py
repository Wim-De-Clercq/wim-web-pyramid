import typing

from marshmallow import ValidationError
from wtforms import Form
from wtforms import StringField
from wtforms.validators import InputRequired
from wtforms.validators import StopValidation

if typing.TYPE_CHECKING:
    from marshmallow import Schema


class SchemaForm(Form):
    schema: 'Schema' = None
    custom_fields = {}

    def load_schema_errors(self, errors):
        for field_name, field_errors in errors.items():
            field = getattr(self, field_name, None)
            if field:
                field.errors = field_errors
            else:
                messages = (f"{field_name}: {error}" for error in field_errors)
                try:
                    self.errors[''].extend(messages)
                except KeyError:
                    self.errors[''] = []
                    self.errors[''].extend(messages)


def initialize_forms():
    form: SchemaForm
    for form in SchemaForm.__subclasses__():
        schema = form.schema
        # noinspection PyProtectedMember
        for field_name, marshmallow_field in schema.fields.items():
            if marshmallow_field.dump_only:
                continue
            field_cls = form.custom_fields.get(field_name, StringField)
            wtforms_field = marshmallow_to_wtforms_field(marshmallow_field,
                                                         field_cls)
            setattr(form, field_name, wtforms_field)


def marshmallow_to_wtforms_field(marshmallow_field, field_cls):
    validators = []
    if marshmallow_field.required:
        validators.append(InputRequired())
    for marshmallow_validator in marshmallow_field.validators:
        validators.append(
            marshmallow_validator_to_wtforms_validator(marshmallow_validator)
        )
    return field_cls(validators=validators)


def marshmallow_validator_to_wtforms_validator(marshmallow_validator):
    def wtform_validator(form, field):
        try:
            # noinspection PyProtectedMember
            marshmallow_validator._validate(field.raw_data)
        except ValidationError as e:
            raise StopValidation('\n'.join(e.messages))
    return wtform_validator

