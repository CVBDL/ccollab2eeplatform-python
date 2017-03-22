"""User settings."""

import json
import os


def read_config_file():
    """Read settings JSON file and return a list of user dict."""
    json_file_path = os.path.join(os.path.dirname(__file__), 'users.json')
    with open(json_file_path) as users_json:
        return json.load(users_json)


class UsersSettings():
    """Class for accessing users settings."""

    users = read_config_file()

    @classmethod
    def get_product_by_login(cls, login_name):
        """Get user's product name by login name.

        Args:
            login_name (str): User's CCollab login name.
        Returns:
            str: User's product name.
        """
        for user in cls.users:
            if user['login_name'] == login_name:
                return user['product_name']
