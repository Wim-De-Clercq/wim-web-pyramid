import re
from typing import Type

from wim_web.web.resources import ItemCreateResource
from wim_web.web.resources import ItemEditResource
from wim_web.web.resources import ItemResource
from wim_web.web.resources import ItemsResource
from wim_web.web.resources import RegisterResource
from wim_web.web.resources import Root
from wim_web.web.resources import UserEditResource
from wim_web.web.resources import UserResource
from wim_web.web.resources import UsersResource


class WebResource(object):

    def __init__(self, regex: str, cls: Type) -> None:
        super().__init__()
        self.regex = re.compile(regex)
        self.cls = cls


resources_tree = {
    WebResource('', Root): {  # /
        WebResource('users', UsersResource): {  # /users
            WebResource('\\d+', UserResource): {
                WebResource('edit', UserEditResource): {
                },
            },
        },
        WebResource('items', ItemsResource): {  # /users
            WebResource('create', ItemCreateResource): {
            },
            WebResource('\\d+', ItemResource): {
                WebResource('edit', ItemEditResource): {
                },
            },
        },
        WebResource('register', RegisterResource): {  # /register
        },
    },
}


def process_tree(tree):
    for resource, child_tree in tree.items():
        for child_resource in child_tree:
            try:
                resource.cls.children.append(child_resource)
            except AttributeError:
                resource.cls.children = []
                resource.cls.children.append(child_resource)

        process_tree(child_tree)


process_tree(resources_tree)
