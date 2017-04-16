#!/usr/bin/python3

import os

def getParsed(rawFile):
    """ Return a dictionnary containing the body part and header part of passed
    file. If there's no header part, an empty string is returned as header part.
    Same for body. If file is bad formatted, None is returned."""

    result = {}
    parsedLines = ""
    splittedFile = rawFile.splitlines()

    firstBodyLine = False
    headerPart = False

    if(splittedFile.pop(0) == "---"):
        # First line of passed file declares a header.
        headerPart = True
    else:
        result["header"] = []
        firstBodyLine = True

    for line in splittedFile:
        if(firstBodyLine and line == ""):
            # First line of the body is empty. Ignore it.
            firstBodyLine = False
            continue

        if(line == "---" and headerPart):
            # Header's end. Save content of header in result["header"] and
            # reinitialize parsedLines for body
            headerPart = False
            firstBodyLine = True
            result["header"] = parsedLines
            parsedLines = ""
            continue

        parsedLines += (line + "\n")

    if(headerPart and "header" not in result.keys()):
        # Header was declared, but never closed. Something's wrong, sorry !
        return None

    result["body"] = parsedLines

    return result
