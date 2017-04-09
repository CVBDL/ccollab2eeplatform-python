"""Charts settings module."""

import json
import os


def read_config_file():
    """Read settings JSON file and return settings."""
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  'charts-settings.json')
    with open(json_file_path) as settings:
        return json.load(settings)


class ChartsSettings:
    """Class for accessing charts settings."""

    settings = read_config_file()

    @classmethod
    def get_settings(cls, key):
        """Return a chart's settings by a key.

        Args:
            key (str): The key for finding settings.
        Returns:
            A dict of settings or None if not found.
        """
        return cls.settings.get(key, None)
