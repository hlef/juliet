#!/usr/bin/python3

import yaml, os, sys, logging
from jinja2 import Environment, FileSystemLoader
from juliet import paths

def configure_jinja(theme, src):
    """ Configure and return Jinja2 Environment. """

    # Do not enable autoescape since we actually *do not* want it. Otherwise, we
    # wouldn't be able to integrate html content in the templates properly.

    themePath = os.path.join(src, paths.THEMES_PATH, theme)
    logging.debug("Setting up environment at " + themePath)

    return Environment(loader=FileSystemLoader(themePath), autoescape=False)

def get_config(cfgFile):
    """ Parse and return passed configuration file. """

    config = {}

    if(not os.path.isfile(cfgFile)):
        sys.exit("Error: Could not find config file: " + cfgFile)

    with open(cfgFile, 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            sys.exit("Error: Failed to parse configuration file: " + str(exc))

    return config
