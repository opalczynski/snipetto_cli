import json
import os

import click
import requests
from click import ClickException

from snipetto.core.configuration import (
    SNIPETTO_HOST,
    SNIPETTO_PATH_CONFIGURATION,
    CONFIG_PATH)


class ActionTypeE:
    LIST = 'list'
    CREATE = 'add'
    EDIT = 'edit'
    DELETE = 'delete'
    GET = 'get'

METHOD_MAP = {
    ActionTypeE.LIST: 'get',
    ActionTypeE.DELETE: 'delete',
    ActionTypeE.EDIT: 'patch',  # safer
    ActionTypeE.GET: 'get',
    ActionTypeE.CREATE: 'post'
}


class APIService:

    def __init__(self):
        self.host = SNIPETTO_HOST
        self.configuration_path = SNIPETTO_PATH_CONFIGURATION
        self.paths = {}
        self.token = None
        self.session = requests.session()

    def _build_url(self, path, instance_id=None):
        if instance_id:
            path = "{path}{instance_id}".format(path=path, instance_id=instance_id)
        if not path.endswith('/'):
            path = "{}/".format(path)
        return "{host}{path}".format(
            host=self.host,
            path=path
        )

    def initialize_paths_mapping(self):
        if not self.paths:
            url = self._build_url(path=self.configuration_path)
            self.paths = self.session.get(url).json()

    def initialize_user(self):
        if not os.path.exists(CONFIG_PATH):
            click.echo('Noticed that you are not initialized yet. '
                       'Please fill out data below')
            username = click.prompt('Provide your username (should be slug)', type=str)
            password = click.prompt('Provide your password', hide_input=True)
            response = self.request('auth', 'init', action=ActionTypeE.CREATE, json={
                'username': username,
                'password': password
            })
            with open(CONFIG_PATH, 'w+') as f:
                f.write(json.dumps(response))
        else:
            with open(CONFIG_PATH, 'r') as f:
                response = json.loads(f.read())
        self.token = response['key']

    def init(self):
        self.initialize_paths_mapping()
        self.initialize_user()

    def make_call(self, path, instance_id=None, method='get', **kwargs):
        http_method = getattr(self.session, method)
        response = http_method(
            self._build_url(
                path=path,
                instance_id=instance_id
            ),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(self.token),
            },
            **kwargs
        )
        if response.status_code in [400, 404, 500]:
            # TODO: make it prettier
            raise ClickException(response.content)
        if response.status_code in [204]:
            return {'info': 'Instance deleted.'}
        return response.json()

    def request(self, app_name, endpoint_name, action=ActionTypeE.LIST, **kwargs):
        path = self.paths[app_name][endpoint_name]
        instance_id = None
        if action in [ActionTypeE.EDIT, ActionTypeE.DELETE, ActionTypeE.GET]:
            instance_id = kwargs.pop('id', None)
            if not instance_id:
                # just in case - should be ok;
                raise ClickException('This action requires instance ID.')
        return self.make_call(path=path, instance_id=instance_id, method=METHOD_MAP[action], **kwargs)
