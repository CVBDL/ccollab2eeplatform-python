"""User settings."""

import json
import os


def list_login_names():
    """Find and list all the login names.

    Returns:
        A list of login names.
    """
    return [user['login_name'] for user in _users]


def get_product_by_login(login_name):
    """Get user's product name by login name.

    Args:
        login_name (str): User's CCollab login name.
    Returns:
        str: User's product name, returns 'Unknown' if user not found.
    """
    for user in _users:
        if user['login_name'] == login_name:
            return user['product_name']
    return 'Unknown'


def _read_config_file():
    """Internal helper that read user config file."""
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  'users-settings.json')
    with open(json_file_path) as settings:
        return json.load(settings)


_users = _read_config_file()
