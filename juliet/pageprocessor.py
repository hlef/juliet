import os, re, yaml, slugify, markdown

class PageProcessor:
    FORBIDDEN_HEADER_ENTRIES = {'body'}
    MARKDOWN_EXTENSIONS = ["codehilite", "tables", "footnotes"]

    def __init__(self, baseurl, file_naming_var):
        self.baseurl = baseurl
        self.file_naming_var = file_naming_var

    @staticmethod
    def _process_baseurl_tags(splitted_body, baseurl):
        """ Process {{ baseurl }} tags in passed body text. """

        result = []

        baseurl_tag = r"(\{\{\s*?baseurl\s*?\}\})"
        regex_baseurl_tag = re.compile(r"(?<!\\)" + baseurl_tag)

        for line in splitted_body:
            line = regex_baseurl_tag.sub(baseurl, line)
            line = PageProcessor._unescape_tags(baseurl_tag, line)
            result.append(line)

        return result

    @staticmethod
    def _unescape_tags(regex_as_string, line):
        """ Unescape tags matching passed regex in passed line. """

        regex_unescape_tag = re.compile(r"\\(" + regex_as_string + ")")
        return regex_unescape_tag.sub(r"\1", line)

    @staticmethod
    def _process_body(splitted_body, baseurl):
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

        # Process baseurl tags
        splitted_body = PageProcessor._process_baseurl_tags(splitted_body, baseurl)

        return markdown.markdown("\n".join(splitted_body), extensions=PageProcessor.MARKDOWN_EXTENSIONS)

    @staticmethod
    def _check_header_content(header):
        """ Raise ValueError if passed header contains invalid entries. """

        set_header = set(header.keys())
        if(not PageProcessor.FORBIDDEN_HEADER_ENTRIES.isdisjoint(set_header)):
            invalid_entries = str(PageProcessor.FORBIDDEN_HEADER_ENTRIES & set_header)
            raise ValueError("Header contains forbidden entries " + invalid_entries)

    @staticmethod
    def _process_header(header, filename, file_naming_var):
        """ Parse passed header. Raise ValueError if header can't be parsed
        properly. """

        parsed_header = {}

        # Set up fallback value for installed_filename, which has to be defined anyways
        parsed_header["installed_filename"] = slugify.slugify(os.path.splitext(filename)[0])

        if(header != ""):
            try:
                parsed_header.update(yaml.load(header, Loader=yaml.FullLoader))
            except yaml.YAMLError as exc:
                raise ValueError("Failed to parse file header: " + str(exc))

            PageProcessor._check_header_content(parsed_header)

            if("permalink" in parsed_header.keys()):
                parsed_header["installed_filename"] = parsed_header["permalink"]
            elif(file_naming_var in parsed_header.keys()):
                # If there's a file_naming_variable entry, provide a slugified form of it.
                parsed_header["installed_filename"] = slugify.slugify(parsed_header[file_naming_var])

        parsed_header["installed_filename"] += ".html"

        return parsed_header

    @staticmethod
    def _get_header_limit(splitted_file):
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

    @staticmethod
    def _get_parsed_header(raw_file, filename, file_naming_var):
        """ TODO """

        splitted_file = raw_file.splitlines()

        # Find header, check and process it
        header_limit = PageProcessor._get_header_limit(splitted_file)
        return PageProcessor._process_header("\n"
               .join(splitted_file[1:header_limit]), filename, file_naming_var)

    def process(self, rawfile, filename):
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

        would be returned as {"key": "value", "body": "<p>bodyContent</p>",
                              "installed_filename": filename.html}.
        """

        def _get_body(raw_file, filename, file_naming_var):
            # Find header, check and process it
            splitted_file = rawfile.splitlines()
            header_limit = PageProcessor._get_header_limit(splitted_file)
            return splitted_file[header_limit+1:]

        result = PageProcessor._get_parsed_header(rawfile, filename, self.file_naming_var)

        # Find body, process it
        body = _get_body(rawfile, filename, self.file_naming_var)
        result["body"] = PageProcessor._process_body(body, self.baseurl)

        result["file-name"] = filename

        return result
