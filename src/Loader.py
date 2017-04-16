#!/usr/bin/python3

import os, yaml
from slugify import slugify
from src import FileParser

def getFromFolder(folder, args):
    """ Return a list of parsed files contained in passed folder.

    Files are represented by dictionnaries generated by FileParser.

    They contain following entries:
     * the body (string), in "body"
     * the file name in "file-name"
     * the header's content (nothing if file has no header)"""

    elements = []
    for sourceFile in os.listdir(folder):
        element = {}
        with open(folder + sourceFile, 'r') as stream:
            # Read raw file
            raw = stream.read()

            # Parse file with FileParser and handle parsing errors.
            parsed = FileParser.getParsed(raw)
            if(parsed == None):
                print("Failed to parse file " + folder + sourceFile)
                exit(1)

            # Get body part and file name
            element["body"] = parsed["body"]
            element["file-name"] = sourceFile

            # Get header part and parse it if not empty
            header = parsed["header"]
            if(header != []):
                # Header isn't empty, parse it and append its entries to the
                # file dictionnary
                try:
                    element = {**element, **yaml.load(header)}
                except yaml.YAMLError as exc:
                    print("Failed to parse file header: " + str(exc))
                    exit(1)

                # If there's a title entry, provide a slugified form of it
                if("title" in element.keys()):
                    element["title-slugified"] = slugify(element["title"])

        elements.append(element)
    return elements