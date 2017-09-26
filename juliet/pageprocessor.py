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

    def _process_pygments(self, splitted_body):
        """ Parse and replace highlight blocks in passed body. Raise ValueError if
        passed body contains invalid pygments blocks. """

        HIGHLIGHT = re.compile("{%\s*?highlight (\w+)\s*?%}")
        ENDHIGHLIGHT = re.compile("{%\s*?endhighlight\s*?%}")
        formatter = HtmlFormatter(linenos=True, cssclass="source")

        result = []
        open_blocks = 0
        reached_endhighlight = False
        current_blocktype = None
        current_buffer = ""
        temporary_buffer = ""

        for line in splitted_body:
            if(ENDHIGHLIGHT.match(line) is not None):
                if(not reached_endhighlight):
                    open_blocks -= 1
                    if(open_blocks < 0):
                        raise ValueError("Failed to parse pygments block: A pygments block was closed, but never opened")
                    elif(open_blocks == 0):
                        reached_endhighlight = True
                else:
                    current_buffer += temporary_buffer
                    temporary_buffer = ""
            elif(HIGHLIGHT.match(line) is not None):
                if(reached_endhighlight):
                    lexer = get_lexer_by_name(current_blocktype, stripall=True)
                    result.append(highlight(current_buffer, lexer, formatter))
                    result += temporary_buffer.splitlines()[1:]
                    reached_endhighlight = False
                    current_buffer = ""
                    temporary_buffer = ""

                open_blocks += 1
                if(open_blocks == 1):
                    current_blocktype = HIGHLIGHT.match(line).groups()[0]
                    continue

            if(reached_endhighlight):
                temporary_buffer += line + "\n"
            elif(open_blocks != 0):
                current_buffer += line + "\n"
            else:
                result.append(line)

        if(reached_endhighlight):
            lexer = get_lexer_by_name(current_blocktype, stripall=True)
            result.append(highlight(current_buffer, lexer, formatter))
            result += temporary_buffer.splitlines()[1:]
            reached_endhighlight = False
            current_buffer = ""
            temporary_buffer = ""

        if(open_blocks != 0):
            raise ValueError("Failed to parse pygments block: A pygments block was opened, but never closed")

        return result

    def _process_body(self, splitted_body, baseurl):
        """ Interpret passed body text as Markdown and return it as HTML. Replace
        all occurences of @BASEURL by passed baseurl. Process Pygments blocks. """

        result = ""

        if(not splitted_body):
            # File is empty. Nothing to do.
            return result

        pygments_processed = self._process_pygments(splitted_body)

        starter = 0
        if(pygments_processed[0] == ""):
            starter = 1

        # TODO This should be in a separate method
        # Go through body. Ignore first line if it is empty
        for line in pygments_processed[starter:]:
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

        parsed_header = {}

        if(header != ""):
            parsed_header = {}

            try:
                parsed_header = yaml.load(header)
            except yaml.YAMLError as exc:
                raise ValueError("Failed to parse file header: " + str(exc))

            self._check_header(parsed_header)

            # If there's a title entry, provide a slugified form of it
            if("title" in parsed_header.keys()):
                parsed_header["slug"] = slugify(parsed_header["title"])

        return parsed_header

    def _get_header_limit(self, splitted_file):
        """ Return the position of header limiter "---". Return -1 if there's no
        header. Raise ValueError if passed file is bad formatted. """

        if(not splitted_file or splitted_file[0] != "---"):
            # File is empty or doesn't start by a header limiter
            return -1

        i = 1

        # Find next header limiter. Ignore first line since we know it is the first
        # header limiter
        for line in splitted_file[1:]:
            if(line == "---"):
                return i
            i+=1

        raise ValueError("Failed to parse header: Header never closed")

    def process(self, raw_file, filename):
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
        splitted_file = raw_file.splitlines()

        # Find header and process it
        header_limit = self._get_header_limit(splitted_file)
        parsed_header = self._process_header("\n".join(splitted_file[1:header_limit]))
        result.update(parsed_header)

        # Find body and process it
        splitted_body = splitted_file[header_limit+1:]
        result["body"] = self._process_body(splitted_body, self.baseurl)

        result["file-name"] = filename

        return result
