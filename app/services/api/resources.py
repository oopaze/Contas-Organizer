from typing import Dict, List
from functools import partial
from collections import namedtuple

import requests


fake_response = namedtuple('Response', "status_code")


class BaseResource:
    actions = {}

    def __init__(self, headers, base_url):
        self.headers = headers
        self.api_base_url = base_url

    def get_action(self, key: str) -> Dict:
        return self.actions[key]

    def generate_action_methods(self):
        for key in self.actions.keys():
            method = self.actions[key]['method']
            url = self.actions[key]['url']

            action_function = partial(self.base_request_action, method=method, url=url)

            setattr(self, key, action_function)

    def base_request_action(
        self,
        method: str,
        url: str,
        data: Dict = {},
        url_params: List = [],
        get_params: Dict = {},
    ):
        url = url.format(*url_params)
        action_url = f"{self.api_base_url}{url}"

        for i, param in enumerate(get_params.items()):
            if i == 0:
                action_url += '?'

            key, value = param
            action_url += f"{key}={value}&"

        request_action = getattr(requests, method.lower())

        kwargs = {"json": data}

        if self.Meta.auth:
            kwargs['headers'] = self.headers
        try:
            return request_action(action_url, **kwargs)
        except:
            return fake_response(status_code=500)

    class Meta:
        name = ""
        plural_name = ""
        auth = False


class UserResource(BaseResource):
    actions = {
        "login": {"method": "POST", "url": "api/v1/token/"},
        "refresh": {"method": "POST", "url": "api/v1/token/refresh/"},
    }

    class Meta:
        name = "user"
        plural_name = "users"
        auth = False


class ContaResource(BaseResource):
    actions = {"create": {"method": "POST", "url": "api/v1/conta/"}}

    class Meta:
        name = "conta"
        plural_name = "contas"
        auth = True


class ParcelaResource(BaseResource):
    actions = {"list": {"method": "GET", "url": "api/v1/parcelas/"}}

    class Meta:
        name = "parcela"
        plural_name = "parcelas"
        auth = True


RESOURCES = [
    (ContaResource.Meta.name, ContaResource),
    (ParcelaResource.Meta.name, ParcelaResource),
    (UserResource.Meta.name, UserResource),
]
