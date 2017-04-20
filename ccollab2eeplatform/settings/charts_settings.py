"""Provide all charts related settings."""

import json
import os


__all__ = ['list_products', 'get_review_settings', 'get_defect_settings']


def read_config_file():
    """Read settings JSON file and return settings."""
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  'charts-settings.json')
    with open(json_file_path) as settings:
        return json.load(settings)


SETTINGS = read_config_file()


def list_products():
    """Return a list of product names."""
    return SETTINGS.get('products', [])


def get_review_settings():
    """Return a dict of review charts settings."""
    return SETTINGS.get('review', None)


def get_defect_settings():
    """Return a dict of defect charts settings."""
    return SETTINGS.get('defect', None)
