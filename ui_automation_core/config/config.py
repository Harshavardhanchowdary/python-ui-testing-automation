import os
import json
from jsonmerge import merge

settings = None
device_config = None


def load_settings_config():
    """


    """
    global settings

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'browser_settings.json')) as f:
        base = json.load(f)

    env_settings_file = os.environ.get('environment_variables', 'environment_variables.json')
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), env_settings_file)) as f:
        head = json.load(f)
    settings = merge(base, head)


def load_device_config():
    """
    Loads the _device_config JSON file and sets the device_config. Device config is used in driver factory.

    """
    global device_config
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_profile.json')) as f:
        device_config = json.load(f)


# calls above functions
load_settings_config()
load_device_config()
