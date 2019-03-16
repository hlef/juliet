import unittest
from juliet.pageprocessor import PageProcessor
from juliet import defaults

class fileParserTest(unittest.TestCase):

    FILENAME = "filename.html"
    baseurl = "/base/url"
    file_naming_variable = defaults.DEFAULT_FILE_NAMING_VARIABLE

    def setUp(self):
        self.processor = PageProcessor(self.baseurl, self.file_naming_variable)

    def test_get_header_limit(self):
        """ Make sure that _get_header_limit() is working well with simple files. """

        splittedFile1 = ["---", "---", "body"]
        splittedFile2 = ["---", "key:value", "---", "body"]
        splittedFile2 = ["---", "key:value", "some42:42", "---"]

        self.assertEqual(1, self.processor._get_header_limit(splittedFile1))
        self.assertEqual(3, self.processor._get_header_limit(splittedFile2))

    def test_get_header_limit_with_invalid_files(self):
        """ Make sure that _get_header_limit() is working well with invalid files. """

        no_header = ["body"]
        self.assertRaises(ValueError, self.processor._get_header_limit, no_header)

        only_one_sep1 = ["---"]
        self.assertRaises(ValueError, self.processor._get_header_limit, only_one_sep1)

        only_one_sep2 = ["", "---"]
        self.assertRaises(ValueError, self.processor._get_header_limit, only_one_sep2)

        only_one_sep3 = ["---", "", "test"]
        self.assertRaises(ValueError, self.processor._get_header_limit, only_one_sep3)

    def test_check_header_content1(self):
        """ Make sure that _check_header_content() is working properly when passing
        invalid headers."""

        invalid_header = {"body": "value"}

        self.assertRaises(ValueError, self.processor._check_header_content, invalid_header)

    def test_check_header_content2(self):
        """ Make sure that _check_header_content() is working properly when passing
        valid headers."""

        valid_header = {"key": "value", "key2": "value2", "foo": "bar"}

        self.processor._check_header_content(valid_header)

    def test_process_header(self):
        """ Make sure that the _process_header() method is working well with
        simple headers."""

        header = """key: value\nkey2: value2\nfoo: bar"""

        result = {"key": "value", "key2": "value2", "foo": "bar", "installed_filename": self.FILENAME}

        self.assertEqual(result, self.processor._process_header(header, self.FILENAME, self.file_naming_variable))

    def test_process_header_with_file_naming_var_defined(self):
        """ Make sure that the _process_header() method is working well with
        simple headers defining the file naming variable."""

        header = """key: value\nkey2: value2\nfoo: bar\ntitle: 'this'"""

        result = {"key": "value", "key2": "value2", "foo": "bar", "title": "this", "installed_filename": "this.html"}

        self.assertEqual(result, self.processor._process_header(header, self.FILENAME, self.file_naming_variable))

    def test_process_header_with_permalink_defined(self):
        """ Make sure that the _process_header() method is working well with
        simple headers defining the permalink variable."""

        header = """foo: bar\npermalink: \"perma\""""
        header2 = """foo: bar\npermalink: \"perma\"\ntitle: this"""

        result = {"foo": "bar", "permalink": "perma", "installed_filename": self.FILENAME}
        result2 = {"foo": "bar", "title": "this", "permalink": "perma", "installed_filename": "this.html"}

        self.assertEqual(result, self.processor._process_header(header, self.FILENAME, self.file_naming_variable))
        self.assertEqual(result2, self.processor._process_header(header2, self.FILENAME, self.file_naming_variable))

    def test_parsing_simple_valid_file(self):
        """ Make sure that process() returns the excepted result when passing
        simple, valid files."""

        validFile = """---\nkey: value\nwhatever: anothervalue\n22i: valuewithnumbers5\n---\n\nbody"""

        result = {"key": "value", "whatever": "anothervalue", "22i": "valuewithnumbers5",
                  "installed_filename": self.FILENAME, "body": "<p>body</p>", 'file-name': self.FILENAME}

        self.assertEqual(result, self.processor.process(validFile, self.FILENAME))

    def test_parsing_valid_without_header_or_body(self):
        """ Make sure that process() returns the excepted result when passing
        simple, valid files with empty header and body."""

        validFile1 = """---\n---\n\nbody"""
        result1 = {"body": "<p>body</p>", 'file-name': self.FILENAME, "installed_filename": self.FILENAME}

        validFile2 = """---\n\n---"""
        result2 = {"body": "", 'file-name': self.FILENAME, "installed_filename": self.FILENAME}

        self.assertEqual(result1, self.processor.process(validFile1, self.FILENAME))
        self.assertEqual(result2, self.processor.process(validFile2, self.FILENAME))

    def test_parsing_invalid_file(self):
        """ Make sure that process() returns None if passed file is invalid."""

        invalidFile = """---\nkey: value\nbody"""

        self.assertRaises(ValueError, self.processor.process, invalidFile, self.FILENAME)

    def test_baseurl_tags_parsing(self):
        """ Make sure that baseurl tags are well parsed. """

        body_with_baseurl1 = ["{{baseurl}}", "{{ baseurl}}", "{{baseurl     }}", "{{    baseurl}}"]
        result_body_with_baseurl1 = [self.baseurl, self.baseurl, self.baseurl, self.baseurl]

        body_with_baseurl2 = ["How, well, here it is: {{ baseurl}}."]
        result_body_with_baseurl2 = ["How, well, here it is: " + self.baseurl + "."]

        body_with_baseurl3 = ["several lines", "{{baseurl }}", "because thats fun"]
        result_body_with_baseurl3 = ["several lines", self.baseurl, "because thats fun"]

        self.assertEqual(result_body_with_baseurl1, self.processor._process_baseurl_tags(body_with_baseurl1, self.baseurl))
        self.assertEqual(result_body_with_baseurl2, self.processor._process_baseurl_tags(body_with_baseurl2, self.baseurl))
        self.assertEqual(result_body_with_baseurl3, self.processor._process_baseurl_tags(body_with_baseurl3, self.baseurl))

    def test_escape_baseurl_tags(self):
        """ Make sure that baseurl tags escaping works. """

        body_with_baseurl1 = [r"\{{ baseurl }} = {{ baseurl }}"]
        result1 = [r"{{ baseurl }} = " + self.baseurl]

        body_with_baseurl2 = [r"\{{ baseurl }}, some text\\{{baseurl}}, and some other TEXT\\\{{baseurl  }}here, and also \\\\{{baseurl}}"]
        result2 = [r"{{ baseurl }}, some text\{{baseurl}}, and some other TEXT\\{{baseurl  }}here, and also \\\{{baseurl}}"]

        self.assertEqual(result1, self.processor._process_baseurl_tags(body_with_baseurl1, self.baseurl))
        self.assertEqual(result2, self.processor._process_baseurl_tags(body_with_baseurl2, self.baseurl))

    def test_escape_pygments_blocks(self):
        """ Make sure that pygments blocks escaping works. """

        body_with_pygments_blocks1 = [r"\{% highlight shell %}\{% endhighlight %}"]
        result1 = [r"{% highlight shell %}{% endhighlight %}"]

        body_with_pygments_blocks2 = [r"\\{% highlight shell %}\\{% endhighlight %}"]
        result2 = [r"\{% highlight shell %}\{% endhighlight %}"]

        body_with_pygments_blocks3 = [r"\\\{% highlight shell %}\\\{% endhighlight %}"]
        result3 = [r"\\{% highlight shell %}\\{% endhighlight %}"]

        self.assertEqual(result1, self.processor._process_pygments(body_with_pygments_blocks1))
        self.assertEqual(result2, self.processor._process_pygments(body_with_pygments_blocks2))
        self.assertEqual(result3, self.processor._process_pygments(body_with_pygments_blocks3))

    def test_invalid_pygments(self):
        """ Make sure that parsing hangs on invalid pygments blocks."""

        opened_but_never_closed = r"""---
---

{% highlight shell %}
cat file"""

        self.assertRaises(ValueError, self.processor.process, opened_but_never_closed, self.FILENAME)

        closed_but_never_opened = """---
---

cat file
{%endhighlight%}"""

        self.assertRaises(ValueError, self.processor.process, closed_but_never_opened, self.FILENAME)

        both_on_the_same_line1 = """---
---

{% highlight shell %}{%endhighlight%}"""

        both_on_the_same_line2 = """---
---

{%endhighlight%}{% highlight shell %}
{%endhighlight%}{% highlight shell %}"""

        both_on_the_same_line3 = """---
---

{%endhighlight%}{% highlight shell %}
{% highlight shell %}{%endhighlight%}"""

        self.assertRaises(ValueError, self.processor.process, both_on_the_same_line1, self.FILENAME)
        self.assertRaises(ValueError, self.processor.process, both_on_the_same_line2, self.FILENAME)
        self.assertRaises(ValueError, self.processor.process, both_on_the_same_line3, self.FILENAME)

    def test_pygments_integration(self):
        """ Make sure that pygments is well integrated in the main process method."""

        file1 = """---
---

{% highlight shell %}
cat file
{% endhighlight  %}
{%highlight shell %}
cat file
{%endhighlight%}"""

        result1 = {"installed_filename": self.FILENAME, "body": """<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file
</pre></div>
</td></tr></table>

<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file
</pre></div>
</td></tr></table>""", 'file-name': self.FILENAME}

        self.assertEqual(result1, self.processor.process(file1, self.FILENAME))

        invalid_inclusion = """---
---

{% highlight shell %}
cat file
{% endhighlight  %}
{% endhighlight  %}"""

        result_invalid_inclusion = {"installed_filename": self.FILENAME, "body": """<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1
2</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file
<span class="o">{</span>% endhighlight  %<span class="o">}</span>
</pre></div>
</td></tr></table>""", 'file-name': self.FILENAME}

        self.assertEqual(result_invalid_inclusion, self.processor.process(invalid_inclusion, self.FILENAME))

        inclusion = """---
---

{% highlight shell %}
cat file
{%highlight shell %}
{% endhighlight  %}
cat file
{%endhighlight%}"""

        result_inclusion = {"installed_filename": self.FILENAME, "body": """<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1\n2\n3\n4</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file\n<span class="o">{</span>%highlight shell %<span class="o">}</span>\n<span class="o">{</span>% endhighlight  %<span class="o">}</span>\ncat file\n</pre></div>\n</td></tr></table>""", 'file-name': self.FILENAME}

        self.assertEqual(result_inclusion, self.processor.process(inclusion, self.FILENAME))
