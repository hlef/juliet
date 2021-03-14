import yaml, os, sys, logging
from jinja2 import Environment, FileSystemLoader
from juliet import paths, defaults

def configure_jinja(theme, src):
    """ Configure and return Jinja2 Environment. """

    # Do not enable autoescape since we actually *do not* want it. Otherwise, we
    # wouldn't be able to integrate html content in the templates properly.

    theme_path = os.path.join(src, paths.THEMES_PATH, theme)
    logging.debug("Setting up environment at " + theme_path)

    return Environment(loader=FileSystemLoader(theme_path), autoescape=False)

def get_yaml(config_file):
    """ Parse and return passed configuration file. """

    # Read config from file
    if(not os.path.isfile(config_file)):
        raise FileNotFoundError("could not find config file: " + config_file)

    config = {}

    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)

    return config

def get_config(config_file):
    """ Parse and return passed configuration file, with checks for sitewide
        config files. """

    def __check_config(config):
        """ Raise exception if passed configuration is invalid. """

        for key, value in defaults.CONFIG_REQUIRED_ENTRIES.items():
            if (key not in config.keys()) or (config[key] == "" and not value):
                raise ValueError("configuration file is missing required key " + key +
                                 " or invalid value was provided")

    config = get_yaml(config_file)

    __check_config(config)

    return config
