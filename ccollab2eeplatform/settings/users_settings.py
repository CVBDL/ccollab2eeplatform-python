"""User settings."""

import json
import os


def read_config_file():
    """Read settings JSON file and return a list of user dict."""
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  'users-settings.json')
    with open(json_file_path) as settings:
        return json.load(settings)


class UsersSettings():
    """Class for accessing users settings."""

    users = read_config_file()

    @classmethod
    def list_login_names(cls):
        """Find and list all the login names.
        
        Returns:
            A list of login names.
        """
        return [ user['login_name'] for user in cls.users ]

    @classmethod
    def get_product_by_login(cls, login_name):
        """Get user's product name by login name.

        Args:
            login_name (str): User's CCollab login name.
        Returns:
            str: User's product name, returns 'Unknown' if user not found.
        """
        for user in cls.users:
            if user['login_name'] == login_name:
                return user['product_name']

        return 'Unknown'
