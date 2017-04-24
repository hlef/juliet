#!/usr/bin/python3

import os, re
from markdown import markdown

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def processPygments(body):
    HIGHLIGHT = re.compile("{%\s*?highlight (\w+)\s*?%}")
    ENDHIGHLIGHT = re.compile("{%\s*?endhighlight\s*?%}")

    result = ""
    bufferedResult = ""
    pygmentsBlock = ""

    for line in body.splitlines():
        if(pygmentsBlock != ""):
            if(ENDHIGHLIGHT.match(line) != None):
                lexer = get_lexer_by_name(pygmentsBlock, stripall=True)
                formatter = HtmlFormatter(linenos=True, cssclass="source")
                result += highlight(bufferedResult, lexer, formatter) + "\n"
                bufferedResult = ""
                pygmentsBlock  = ""
            else:
                bufferedResult += line + "\n"
            continue

        if(HIGHLIGHT.match(line) != None):
            pygmentsBlock = HIGHLIGHT.match(line).groups()[0]
            continue

        result += line + "\n"

    if(pygmentsBlock != ""):
        return None

    return result


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

    parsedLines = processPygments(parsedLines)

    if((headerPart and "header" not in result.keys()) or parsedLines == None):
        # Header was declared, but never closed. Something gone wrong.
        return None

    result["body"] = markdown(parsedLines)

    return result
