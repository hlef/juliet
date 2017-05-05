#!/usr/bin/python3

import os, sys, logging
from juliet.pageprocessor import PageProcessor

def getFromFolder(folder, config):
    """ Load files contained in passed folder, pre-process them using fileParser
    and return them as a list sorted in inverse alphabetical order.

    Files in passed folder should have a valid Page format (see FileParser). """

    elements = []
    entries = sorted(os.listdir(folder), reverse=True)

    processor = PageProcessor(config["site"]["baseurl"])

    for sourceFile in entries:
        logging.debug("Loading file " + sourceFile)

        element = {}
        with open(os.path.join(folder, sourceFile), 'r') as stream:
            raw = stream.read()

            try:
                element = processor.process(raw, sourceFile)
            except ValueError as err:
                sys.exit("Error while loading " + sourceFile + ": " + str(err))

        elements.append(element)
    return elements
