#!/usr/bin/python3

import os
from markdown import markdown

def getParsed(rawFile, baseurl):
    """ Return a parsed form of passed page file.

    Passed file should have the following format:

    ""
    ---
    HEADER, 0->* lines of "key: value" entries.
    ---

    BODY, 0->* lines of markdown content.
    ""

    Returned file is represented by a dictionnary containing following entries:
     * "body": a string containing the markdown body converted to HTML
     * the header's content (nothing if file has no header)

     For example, following file

     ""
     ---
     key: value
     ---

     bodyContent
     ""

     would be returned as {"key": "value", "body": "bodyContent"}

     If there's no body part, an empty string is returned in "body".

     If file is bad formatted, None is returned.
     """

    result = {}
    parsedLines = ""
    splittedFile = rawFile.splitlines()

    firstBodyLine = False
    headerPart = False

    if(splittedFile[0] == "---"):
        # First line of passed file declares a header.
        splittedFile.pop(0)
        headerPart = True
    else:
        # File has no header. Directly parse body.
        result["header"] = []
        firstBodyLine = True

    for line in splittedFile:
        if(firstBodyLine):
            # line is the first line of body part.
            firstBodyLine = False
            if(line == ""):
                # First line of the body is empty. Ignore it.
                continue

        if(line == "---" and headerPart):
            # Header's end. Save content of header in result["header"] and
            # reinitialize parsedLines for body
            headerPart = False
            firstBodyLine = True
            result["header"] = parsedLines
            parsedLines = ""
            continue

        line = line.replace("@BASEURL", baseurl)
        parsedLines += (line + "\n")

    if(headerPart and "header" not in result.keys()):
        # Header was declared, but never closed. Something gone wrong.
        return None

    result["body"] = markdown(parsedLines)

    return result
