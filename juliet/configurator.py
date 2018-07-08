#!/usr/bin/python3

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

def get_config(config_file):
    """ Parse and return passed configuration file. """

    config = {}

    # Read config from file
    if(not os.path.isfile(config_file)):
        raise FileNotFoundError("could not find config file: " + config_file)

    with open(config_file, 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            sys.exit("Error: Failed to parse configuration file: " + str(exc))

    return config
