"""Provide all charts related settings."""

import json
import os


__all__ = ['list_products', 'get_review_settings', 'get_defect_settings']


def list_products():
    """Return a list of product names."""
    return _settings.get('products', [])


def list_injection_stages():
    """Return a list of injection stages."""
    return _settings.get('defect_injection_stage', [])


def get_review_settings():
    """Return a dict of review charts settings."""
    return _settings.get('review', None)


def get_defect_settings():
    """Return a dict of defect charts settings."""
    return _settings.get('defect', None)


def _read_config_file():
    """Internal helper to read settings JSON file and return settings."""
    json_file_path = os.path.join(os.path.dirname(__file__),
                                  'charts-settings.json')
    with open(json_file_path) as settings:
        return json.load(settings)


_settings = _read_config_file()
