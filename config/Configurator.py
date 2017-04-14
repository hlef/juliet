#!/usr/bin/python3

import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

CFG_FILE = "config.yml"

def configureJinja(config):
    """ Configure and return Jinja2 Environment. """

    return Environment(
        loader=PackageLoader('juliet', "themes/" + config["theme"] + "/templates"),
        autoescape=select_autoescape(['html', 'xml'])
    )

def getConfig():
    """ Return parsed config file. """

    config = dict()

    with open(CFG_FILE) as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print("Failed to parse configuration file: " + str(exc))
            exit(1)

    return config
