#!/usr/bin/python3

import os, sys, logging, juliet
from juliet.pageprocessor import PageProcessor

def get_from_folder(folder, config):
    """ Load files contained in passed folder, pre-process them using fileParser
    and return them as a list sorted in inverse alphabetical order.

    Files in passed folder should have a valid Page format (see FileParser). """

    elements = []
    entries = sorted(os.listdir(folder), reverse=True)

    file_naming_var = ""
    if ("file_naming_variable" in config["site"].keys()):
        file_naming_var = config["site"]["file_naming_variable"]
    else:
        file_naming_var = juliet.defaults.DEFAULT_FILE_NAMING_VARIABLE
    processor = PageProcessor(config["site"]["baseurl"], file_naming_var)

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
