#!/usr/bin/python3

import os, re, yaml
from slugify import slugify
from markdown import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class PageProcessor:
    FORBIDDEN_HEADER_ENTRIES = {'body'}

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def _process_pygments(self, splittedBody):
        """ Parse and replace highlight blocks in passed body. Raise ValueError if
        passed body contains invalid pygments blocks. """

        HIGHLIGHT = re.compile("{%\s*?highlight (\w+)\s*?%}")
        ENDHIGHLIGHT = re.compile("{%\s*?endhighlight\s*?%}")

        result = []
        bufferedResult = ""
        pygmentsBlock = ""

        for line in splittedBody:
            if(pygmentsBlock != ""):
                if(ENDHIGHLIGHT.match(line) is not None):
                    lexer = get_lexer_by_name(pygmentsBlock, stripall=True)
                    formatter = HtmlFormatter(linenos=True, cssclass="source")
                    result.append(highlight(bufferedResult, lexer, formatter))
                    bufferedResult = ""
                    pygmentsBlock  = ""
                else:
                    bufferedResult += line + "\n"
                continue

            if(HIGHLIGHT.match(line) is not None):
                pygmentsBlock = HIGHLIGHT.match(line).groups()[0]
                continue

            result.append(line)

        if(pygmentsBlock != ""):
            raise ValueError("Failed to parse pygments block: A pygments block was opened, but never closed")

        return result

    def _process_body(self, splittedBody, baseurl):
        """ Interpret passed body text as Markdown and return it as HTML. Replace
        all occurences of @BASEURL by passed baseurl. Process Pygments blocks. """

        result = ""

        if(not splittedBody):
            # File is empty. Nothing to do.
            return result

        pygmentsProcessed = self._process_pygments(splittedBody)

        starter = 0
        if(pygmentsProcessed[0] == ""):
            starter = 1

        # Go through body. Ignore first line if it is empty
        for line in pygmentsProcessed[starter:]:
            line = line.replace("@BASEURL", baseurl)
            result += line + "\n"

        return markdown(result)

    def _check_header(self, header):
        """ Raise ValueError if passed header contains invalid entries. """

        set_header = set(header.keys())
        if(not self.FORBIDDEN_HEADER_ENTRIES.isdisjoint(set_header)):
            invalid_entries = str(self.FORBIDDEN_HEADER_ENTRIES & set_header)
            raise ValueError("Header contains forbidden entries " + invalid_entries)

    def _process_header(self, header):
        """ Parse passed header."""

        parsedHeader = {}

        if(header != ""):
            parsedHeader = {}

            try:
                parsedHeader = yaml.load(header)
            except yaml.YAMLError as exc:
                raise ValueError("Failed to parse file header: " + str(exc))

            self._check_header(parsedHeader)

            # If there's a title entry, provide a slugified form of it
            if("title" in parsedHeader.keys()):
                parsedHeader["slug"] = slugify(parsedHeader["title"])

        return parsedHeader

    def _get_header_limit(self, splittedFile):
        """ Return the position of header limiter "---". Return -1 if there's no
        header. Raise ValueError if passed file is bad formatted. """

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

        raise ValueError("Failed to parse header: Header never closed")

    def process(self, rawFile, filename):
        """ Return a parsed form of passed page file. Passed file should have the
        following format:

        ""
        ---
        HEADER, 0->* lines of "key: value" entries.
        ---

        BODY, 0->* lines of markdown content.
        ""

        A ValueError is raised if file is bad formatted.

        Returned file is represented by a dictionnary containing following entries:
         * "body": a string containing the markdown body converted to HTML (empty if
         file has no body). Pygments blocks are processed.
         * the header's content.

         For instance, the following file

         ""
         ---
         key: value
         ---

         bodyContent
         ""

         would be returned as {"key": "value", "body": "<p>bodyContent</p>"}.
         """

        result = {}
        splittedFile = rawFile.splitlines()

        # Find header and process it
        headerLimit = self._get_header_limit(splittedFile)
        parsedHeader = self._process_header("\n".join(splittedFile[1:headerLimit]))
        result.update(parsedHeader)

        # Find body and process it
        splittedBody = splittedFile[headerLimit+1:]
        result["body"] = self._process_body(splittedBody, self.baseurl)

        result["file-name"] = filename

        return result
