"""
Registers schema-related parameters for pyramid view configs.

This is meant to to be included in the pyramid config.

Extra parameters supported:
- body_schema: for validating the incoming json body.
- querystring_schema: for validating the incoming query parameters.
- header_schema: for validating the incoming request headers.
- response_schema: for turning the view's response into json.

Each parameter can be given either a marshmallow schema class, or an
   instance.

"""
import inspect
import functools

import marshmallow
from marshmallow import validate

from wim_web.web.views import View


required = validate.Length(min=1, error='Required')


class WebSchema(marshmallow.Schema):

    def __init__(self, *, request_method, only=None, exclude=(), many=False,
                 context=None, load_only=(), dump_only=(), partial=False,
                 unknown=None):
        fields = self._declared_fields
        cfg_dump_only = set()
        cfg_load_only = set()
        required_fields = set()
        for field_name, field in fields.items():
            load_on = field.metadata.get('load_on', [])
            dump_on = field.metadata.get('dump_on', [])
            required_on = field.metadata.get('required_on', [])
            if not dump_on and not load_on:
                msg = "Set at least 'load_on' or 'dump_on' on the field."
                raise ValueError(msg)
            if dump_on and not load_on:
                field.dump_only = True
            if load_on and not dump_on:
                field.load_only = True
            if 'ALL' in required_on or request_method in required_on:
                required_fields.add(field_name)
            if 'ALL' in load_on or request_method in load_on:
                cfg_load_only.add(field_name)
            if 'ALL' in dump_on or request_method in dump_on:
                cfg_dump_only.add(field_name)
        all_fields = only or list(cfg_dump_only.union(cfg_load_only))
        load_only = load_only or (cfg_load_only - cfg_dump_only)
        dump_only = dump_only or (cfg_dump_only - cfg_load_only)
        super().__init__(only=all_fields, exclude=exclude, many=many,
                         context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown)
        for field_name, field in self.fields.items():
            if field_name in required_fields:
                field.required = True


def auto_schema(body_schema=None, querystring_schema=None, header_schema=None,
                response_schema=None):
    def auto_schema_view(view_function):
        validators = []
        res_schema = response_schema

        if body_schema:
            schema = ensure_instance(body_schema)
            validators.append(
                functools.partial(_validate_body, schema)
            )
        if querystring_schema:
            schema = ensure_instance(querystring_schema)
            validators.append(
                functools.partial(_validate_querystring, schema)
            )
        if header_schema:
            schema = ensure_instance(header_schema)
            validators.append(
                functools.partial(_validate_querystring, schema)
            )
        if res_schema:
            res_schema = ensure_instance(res_schema)

        if validators or res_schema:
            @functools.wraps(view_function)
            def wrapper_view(view: View):
                view.request.loaded = {}
                for validator in validators:
                    validator(view.request)

                # Add response_schema to the request, so the view can edit
                # parameters if required.
                view.request.response_schema = res_schema
                response = view_function(view)
                if res_schema:
                    response = res_schema.dump(response)
                return response
            return wrapper_view
        return view_function
    return auto_schema_view


def ensure_instance(class_or_instance):
    if inspect.isclass(class_or_instance):
        return class_or_instance()
    return class_or_instance


def _validate_body(schema, request):
    if 'application/json' in request.content_type:
        data = request.json_body
    else:
        data = request.POST
    result = schema.load(data)
    request.loaded['body'] = result


def _validate_querystring(schema, request):
    result = schema.load(request.GET.mixed())
    request.loaded['querystring'] = result
