#!/usr/bin/python3

import os, sys, logging
from juliet import fileParser

def getFromFolder(folder, config):
    """ Return a list of parsed files contained in passed folder.

    Files in passed folder should have a valid Page format (see FileParser)
    since they will be parsed by FileParser.

    The returned list of files is sorted in inverse order. """

    elements = []
    entries = sorted(os.listdir(folder), reverse=True)
    for sourceFile in entries:
        logging.debug("Loading file " + sourceFile)

        element = {}
        with open(folder + "/" + sourceFile, 'r') as stream:
            raw = stream.read()

            try:
                element = fileParser.process(raw, sourceFile, config["site"]["baseurl"])
            except ValueError as err:
                sys.exit("Error while loading " + sourceFile + ": " + str(err))

        elements.append(element)
    return elements
