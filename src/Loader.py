#!/usr/bin/python3

import os, yaml, slugify
from src import FileParser

def getFromFolder(folder, args):
    elements = []
    for sourceFile in os.listdir(folder):
        element = {}
        with open(folder + sourceFile, 'r') as stream:
            raw = stream.read()

            # Get body
            parsed = FileParser.getParsed(raw)
            if(parsed == None):
                print("Failed to parse file " + folder + sourceFile)
                exit(1)

            element["body"] = parsed["body"]

            # Get and parse header
            header = parsed["header"]
            try:
                element = {**element, **yaml.load(header)}
            except yaml.YAMLError as exc:
                print("Failed to parse file header: " + str(exc))
                exit(1)

            # Slugify title
            element["title-slugified"] = slugify.slugify(element["title"])

        elements.append(element)
    return elements
