"""EagleEye Platform settings module."""

import json
import os


def read_config_file():
    """Read settings JSON file and return settings."""
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  'eeplatform-settings.json')
    with open(json_file_path) as settings:
        return json.load(settings)


class EEPlatformSettings:
    """Class for accessing EagleEye Platform API settings."""

    settings = read_config_file()

    @classmethod
    def get_api_root_endpoint(cls):
        """Return a string of API root endpoint."""
        return cls.settings['api_root_endpoint']
