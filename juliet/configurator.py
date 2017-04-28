#!/usr/bin/python3

import yaml, os
from jinja2 import Environment, FileSystemLoader
from juliet import paths

def configureJinja(config):
    """ Configure and return Jinja2 Environment.

    Do not enable autoescape since we actually *do not* want it. Otherwise, we
    wouldn't be able to integrate html content in the templates proprely. """

    return Environment(
        loader=FileSystemLoader("./" + paths.THEMES_PATH + "/" + config["theme"]),
        autoescape=False)

def getConfig(cfgFile):
    """ Return parsed config file. """

    config = {}

    if(not os.path.isfile(cfgFile)):
        print("Error: Could not find config file: " + cfgFile)
        exit(1)

    with open(cfgFile, 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print("Failed to parse configuration file: " + str(exc))
            exit(1)

    return config
