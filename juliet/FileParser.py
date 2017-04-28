#!/usr/bin/python3

import os, re
from markdown import markdown

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def _processPygments(splittedBody):
    """ Parse and replace highlight blocks in passed body."""

    HIGHLIGHT = re.compile("{%\s*?highlight (\w+)\s*?%}")
    ENDHIGHLIGHT = re.compile("{%\s*?endhighlight\s*?%}")

    result = []
    bufferedResult = ""
    pygmentsBlock = ""

    for line in splittedBody:
        if(pygmentsBlock != ""):
            if(ENDHIGHLIGHT.match(line) != None):
                lexer = get_lexer_by_name(pygmentsBlock, stripall=True)
                formatter = HtmlFormatter(linenos=True, cssclass="source")
                result.append(highlight(bufferedResult, lexer, formatter))
                bufferedResult = ""
                pygmentsBlock  = ""
            else:
                bufferedResult += line + "\n"
            continue

        if(HIGHLIGHT.match(line) != None):
            pygmentsBlock = HIGHLIGHT.match(line).groups()[0]
            continue

        result.append(line)

    if(pygmentsBlock != ""):
        # A pygments block was opened, but never closed
        return None

    return result

def _processBody(splittedBody, baseurl):
    """ Interpret passed body text as Markdown and return it as HTML. Replace
    all occurences of @BASEURL by passed baseurl. """

    result = ""

    if(not splittedBody):
        # File is empty. Nothing to do.
        return result

    starter = 0
    if(splittedBody[0] == ""):
        starter = 1

    # Go through body. Ignore first line if it is empty
    for line in splittedBody[starter:]:
        line = line.replace("@BASEURL", baseurl)
        result += line + "\n"

    return markdown(result)

def _getHeaderLimit(splittedFile):
    """ Return the position of header limiter "---". Return -1 if there's no
    header, None if passed file is bad formatted."""

    if(not splittedFile or splittedFile[0] != "---"):
        # File is empty or doesn't start by a header limiter
        return -1

    i = 1

    # Find next header limiter. Ignore first line since we know it is the first
    # header limiter
    for line in splittedFile[1:]:
        if(line == "---"):
            return i
        i+=1

    return None

def process(rawFile, baseurl):
    """ Return a parsed form of passed page file.

    Passed file should have the following format:

    ""
    ---
    HEADER, 0->* lines of "key: value" entries.
    ---

    BODY, 0->* lines of markdown content.
    ""

    Returned file is represented by a dictionnary containing following entries:
     * "body": a string containing the markdown body converted to HTML (empty if
     file has no body)
     * "header": a string caintaining the header's content (empty if file has no
     header)

     For example, following file

     ""
     ---
     key: value
     ---

     bodyContent
     ""

     would be returned as {"header": "key: value", "body": "<p>bodyContent</p>"}

     If file is bad formatted, None is returned.
     """

    result = {}
    splittedFile = rawFile.splitlines()

    headerLimit = _getHeaderLimit(splittedFile)

    if(headerLimit is None):
        # Bad formatted file
        return None

    result["header"] = "\n".join(splittedFile[1:headerLimit])

    pygmentsProcessed = _processPygments(splittedFile[headerLimit+1:])
    result["body"] = _processBody(pygmentsProcessed, baseurl)

    return result
