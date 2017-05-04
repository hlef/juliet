#!/usr/bin/python3

import yaml, os, sys
from jinja2 import Environment, FileSystemLoader
from juliet import paths

def configureJinja(theme):
    """ Configure and return Jinja2 Environment. Takes the theme directory as
    argument. """

    # Do not enable autoescape since we actually *do not* want it. Otherwise, we
    # wouldn't be able to integrate html content in the templates properly.

    return Environment(
        loader=FileSystemLoader("./" + paths.THEMES_PATH + "/" + theme),
        autoescape=False)

def getConfig(cfgFile):
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
