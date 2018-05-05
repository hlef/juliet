#!/usr/bin/python3

import os, re, yaml, slugify, markdown, pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class PageProcessor:
    FORBIDDEN_HEADER_ENTRIES = {'body'}

    def __init__(self, baseurl, file_naming_variable):
        self.baseurl = baseurl
        self.file_naming_variable = file_naming_variable

    def _process_pygments(self, splitted_body):
        """ Process highlight blocks in passed body. Raise ValueError if
        passed body contains invalid pygments blocks. """

        # FIXME Ugly looking method. This is way too big, and pretty ununderstandable.

        escaped = r"(\\)+"
        highlight = r"\{%\s*?highlight (\w+)\s*?%\}"
        endhighlight = r"\{%\s*?endhighlight\s*?%\}"
        regex_highlight = re.compile(highlight)
        regex_endhighlight = re.compile(endhighlight)
        regex_escaped_highlight = re.compile(escaped + highlight)
        regex_escaped_endhighlight = re.compile(escaped + endhighlight)
        formatter = HtmlFormatter(linenos=True, cssclass="source")

        result = []
        open_blocks = 0
        reached_endhighlight = False
        current_lexer = None
        current_buffer = ""
        temporary_buffer = ""

        for line in splitted_body:
            if(regex_escaped_endhighlight.match(line) is not None or regex_escaped_highlight.match(line) is not None):
                line = self._unescape_tags(endhighlight, line)
                line = self._unescape_tags(highlight, line)

            elif(regex_endhighlight.match(line) is not None):
                if(not reached_endhighlight):
                    open_blocks -= 1
                    if(open_blocks < 0):
                        raise ValueError("Failed to parse pygments block: A pygments block was closed, but never opened")
                    elif(open_blocks == 0):
                        reached_endhighlight = True
                else:
                    current_buffer += temporary_buffer
                    temporary_buffer = ""

            elif(regex_highlight.match(line) is not None):
                if(reached_endhighlight):
                    result.append(pygments.highlight(current_buffer, current_lexer, formatter))
                    result += temporary_buffer.splitlines()[1:]
                    reached_endhighlight = False
                    current_buffer = ""
                    temporary_buffer = ""

                open_blocks += 1
                if(open_blocks == 1):
                    block_type = regex_highlight.match(line).groups()[0]
                    current_lexer = get_lexer_by_name(block_type, stripall=True)
                    continue

            if(reached_endhighlight):
                temporary_buffer += line + "\n"
            elif(open_blocks != 0):
                current_buffer += line + "\n"
            else:
                result.append(line)

        if(reached_endhighlight):
            result.append(pygments.highlight(current_buffer, current_lexer, formatter))
            result += temporary_buffer.splitlines()[1:]

        if(open_blocks != 0):
            raise ValueError("Failed to parse pygments block: A pygments block was opened, but never closed")

        return result

    def _process_baseurl_tags(self, splitted_body, baseurl):
        """ Process {{ baseurl }} tags in passed body text. """

        result = []

        baseurl_tag = r"(\{\{\s*?baseurl\s*?\}\})"
        regex_baseurl_tag = re.compile(r"(?<!\\)" + baseurl_tag)

        for line in splitted_body:
            line = regex_baseurl_tag.sub(baseurl, line)
            line = self._unescape_tags(baseurl_tag, line)
            result.append(line)

        return result

    def _unescape_tags(self, regex_as_string, line):
        """ Unescape tags matching passed regex in passed line. """

        regex_unescape_tag = re.compile(r"\\(" + regex_as_string + ")")
        return regex_unescape_tag.sub(r"\1", line)

    def _process_body(self, splitted_body, baseurl):
        """ Return fully HTML-converted passed body text.
        First preprocess it using Pygments and replace {{ baseurl }} tags,
        then markdown process it using markdown library. """

        if(not splitted_body):
            # File is empty. Nothing to do.
            return ""

        # Remove first line if blank.
        starter = 0
        if(splitted_body[0] == ""):
            starter = 1

        splitted_body = splitted_body[starter:]

        # Process Pygments blocks
        splitted_body = self._process_pygments(splitted_body)

        # Process baseurl tags
        splitted_body = self._process_baseurl_tags(splitted_body, baseurl)

        return markdown.markdown("\n".join(splitted_body))

    def _check_header_content(self, header):
        """ Raise ValueError if passed header contains invalid entries. """

        set_header = set(header.keys())
        if(not self.FORBIDDEN_HEADER_ENTRIES.isdisjoint(set_header)):
            invalid_entries = str(self.FORBIDDEN_HEADER_ENTRIES & set_header)
            raise ValueError("Header contains forbidden entries " + invalid_entries)

    def _process_header(self, header, filename):
        """ Parse passed header. Raise ValueError if header can't be parsed
        properly. """

        parsed_header = {}

        # Set up fallback value for slug, which has to be defined anyways
        parsed_header["slug"] = slugify.slugify(os.path.splitext(filename)[0])

        if(header != ""):
            try:
                parsed_header.update(yaml.load(header))
            except yaml.YAMLError as exc:
                raise ValueError("Failed to parse file header: " + str(exc))

            self._check_header_content(parsed_header)

            if(self.file_naming_variable in parsed_header.keys()):
                # If there's a file_naming_variable entry, provide a slugified form of it.
                parsed_header["slug"] = slugify.slugify(parsed_header[self.file_naming_variable])

        return parsed_header

    def _get_header_limit(self, splitted_file):
        """ Return line number of the last header limiter "---" starting by 0.
        Raise ValueError if passed file is bad formatted. """

        if(not splitted_file or splitted_file[0] != "---"):
            # File is empty or doesn't start by a header limiter
            raise ValueError("Failed to parse file header: no header.")

        i = 1

        # Find next header limiter. Ignore first line since we know it is the first
        # header limiter
        for line in splitted_file[1:]:
            if(line == "---"):
                return i
            i+=1

        raise ValueError("Failed to parse header: Header never closed")

    def process(self, raw_file, filename):
        """ Return a parsed form of passed file.

        ### 1) Format
        Passed file should have the following format:

        ""
         ---
         HEADER, 0->* lines of "key: value" entries.
         ---

         BODY, 0->* lines of markdown content.
        ""

        Even if header part is empty, it should be present.

        For example, ""BODY"" or

        ""---
         BODY""

        are *not* valid files.

        ### 2) Returned value
        A ValueError is raised if file is bad formatted.

        Returned file is represented by a dictionnary containing following entries:
         * "body": a string containing the markdown body converted to HTML (empty if
           file has no body). Pygments blocks are processed.
         * the header's content.

        ### 3) Examples
        The following file

        ""---
          key: value
          ---
          bodyContent""

        would be returned as {"key": "value", "body": "<p>bodyContent</p>", "slug": filename}. """

        result = {}
        splitted_file = raw_file.splitlines()

        # Find header, check and process it
        header_limit = self._get_header_limit(splitted_file)
        parsed_header = self._process_header("\n".join(splitted_file[1:header_limit]), filename)
        result.update(parsed_header)

        # Find body, process it
        splitted_body = splitted_file[header_limit+1:]
        result["body"] = self._process_body(splitted_body, self.baseurl)

        result["file-name"] = filename

        return result
