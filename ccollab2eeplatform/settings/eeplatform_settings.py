"""EagleEye Platform settings module."""

import json
import os


__all__ = ['get_api_root_endpoint']


def get_api_root_endpoint():
    """Return a string of API root endpoint."""
    return _settings.get('api_root_endpoint', None)


def _read_config_file():
    """Internal helper to read settings JSON file and return settings."""
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  'eeplatform-settings.json')
    with open(json_file_path) as settings:
        return json.load(settings)


_settings = _read_config_file()
