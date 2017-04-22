#!/usr/bin/python3

import yaml
from jinja2 import Environment, FileSystemLoader

CFG_FILE = "config.yml"

def configureJinja(config):
    """ Configure and return Jinja2 Environment.

    Do not enable autoescape since we actually *do not* want it. Otherwise, we
    wouldn't be able to integrate our html content in the templates proprely. """

    return Environment(
        loader=FileSystemLoader("./themes/" + config["theme"]),
        autoescape=False)

def getConfig():
    """ Return parsed config file. """

    config = {}

    with open(CFG_FILE, 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print("Failed to parse configuration file: " + str(exc))
            exit(1)

    return config
