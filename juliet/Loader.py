#!/usr/bin/python3

import os, yaml
from slugify import slugify
from juliet import FileParser

def getFromFolder(folder, config):
    """ Return a list of parsed files contained in passed folder.

    Files in passed folder should have a valid Page format (see FileParser)
    since they will be parsed by FileParser.

    The returned list of files is sorted in inverse order.

    Returned files also have a "file-name" entry containing their file name. """

    elements = []
    entries = sorted(os.listdir(folder), reverse=True)
    for sourceFile in entries:
        element = {}
        with open(folder + sourceFile, 'r') as stream:
            # Read raw file
            raw = stream.read()

            # Parse file with FileParser and handle parsing errors.
            parsed = FileParser.getParsed(raw, config["site"]["baseurl"])
            if(parsed == None):
                print("Failed to parse file " + folder + sourceFile)
                exit(1)

            # Get body part, get file name
            element["body"] = parsed["body"]
            element["file-name"] = sourceFile

            # Get header part and parse it if not empty
            header = parsed["header"]
            if(header != ""):
                # Header isn't empty, parse it and append its entries to the
                # file dictionnary
                try:
                    element = {**element, **yaml.load(header)}
                except yaml.YAMLError as exc:
                    print("Failed to parse file header: " + str(exc))
                    exit(1)

                # If there's a title entry, provide a slugified form of it
                if("title" in element.keys()):
                    element["slug"] = slugify(element["title"])

        elements.append(element)
    return elements
