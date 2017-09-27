import unittest
from juliet.pageprocessor import PageProcessor

class fileParserTest(unittest.TestCase):

    FILENAME = "filename"

    def setUp(self):
        self.processor = PageProcessor("/base/url")

    def test_get_header_limit1(self):
        """ Make sure that _get_header_limit() is working well with simple files. """

        splittedFile1 = ["---", "---", "body"]
        splittedFile2 = ["body"]
        splittedFile3 = ["---", "key:value", "---", "body"]

        self.assertEqual(1, self.processor._get_header_limit(splittedFile1))
        self.assertEqual(-1, self.processor._get_header_limit(splittedFile2))
        self.assertEqual(2, self.processor._get_header_limit(splittedFile3))

    def test_check_header1(self):
        """ Make sure that _check_header() is working properly when passing
        invalid headers."""

        invalid_header = {"body": "value"}

        self.assertRaises(ValueError, self.processor._check_header, invalid_header)

    def test_check_header2(self):
        """ Make sure that _check_header() is working properly when passing
        valid headers."""

        valid_header = {"key": "value", "key2": "value2", "foo": "bar"}

        self.processor._check_header(valid_header)

    def test_process_header1(self):
        """ Make sure that the _process_header() method is working well with
        simple headers."""

        header = """key: value
key2: value2
foo: bar"""

        result = {"key": "value", "key2": "value2", "foo": "bar"}

        self.assertEqual(result, self.processor._process_header(header))

    def test_parsing_valid_file1(self):
        """ Make sure that process() returns the excepted result when passing
        simple, valid files."""

        validFile = """---
key: value
whatever: anothervalue
22i: valuewithnumbers5
---

body"""

        result = {"key": "value", "whatever": "anothervalue", "22i": "valuewithnumbers5",
                  "body": "<p>body</p>", 'file-name': self.FILENAME}

        self.assertEqual(result, self.processor.process(validFile, self.FILENAME))

    def test_parsing_valid_file2(self):
        """ Make sure that process() returns the excepted result when passing
        simple, valid files with empty header and body."""

        validFile1 = """---
---

body"""

        validFile2 = """body"""

        result1 = {"body": "<p>body</p>", 'file-name': self.FILENAME}

        validFile3 = """---

---"""

        result3 = {"body": "", 'file-name': self.FILENAME}

        validFile4 = """"""

        result4 = {"body": "", 'file-name': self.FILENAME}

        self.assertEqual(result1, self.processor.process(validFile1, self.FILENAME))
        self.assertEqual(result1, self.processor.process(validFile2, self.FILENAME))
        self.assertEqual(result3, self.processor.process(validFile3, self.FILENAME))
        self.assertEqual(result4, self.processor.process(validFile4, self.FILENAME))

    def test_parsing_invalid_file(self):
        """ Make sure that process() returns None if passed file is invalid."""

        invalidFile = """---
key: value

body"""

        self.assertRaises(ValueError, self.processor.process, invalidFile, self.FILENAME)

    def test_baseurl_tags_parsing(self):
        """ Make sure that baseurl tags are well parsed. """

        baseurl = "/home/user/test/"

        body_with_baseurl1 = ["{{baseurl}}",
                              "{{ baseurl}}",
                              "{{baseurl     }}",
                              "{{    baseurl}}"]

        result_body_with_baseurl1 = [baseurl, baseurl, baseurl, baseurl]

        body_with_baseurl2 = ["How, well, here it is: {{ baseurl}}."]

        result_body_with_baseurl2 = ["How, well, here it is: " + baseurl + "."]

        body_with_baseurl3 = ["several lines", "{{baseurl }}", "because thats fun"]

        result_body_with_baseurl3 = ["several lines", baseurl, "because thats fun"]

        self.assertEqual(result_body_with_baseurl1, self.processor._process_baseurl_tags(body_with_baseurl1, baseurl))
        self.assertEqual(result_body_with_baseurl2, self.processor._process_baseurl_tags(body_with_baseurl2, baseurl))
        self.assertEqual(result_body_with_baseurl3, self.processor._process_baseurl_tags(body_with_baseurl3, baseurl))

    def test_invalid_pygments(self):
        """ Make sure that parsing hangs on invalid pygments blocks."""

        opened_but_never_closed = """---
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

        result1 = {"body": """<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file
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

        result_invalid_inclusion = {"body": """<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1
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

        result_inclusion = {"body": """<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1\n2\n3\n4</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file\n<span class="o">{</span>%highlight shell %<span class="o">}</span>\n<span class="o">{</span>% endhighlight  %<span class="o">}</span>\ncat file\n</pre></div>\n</td></tr></table>""", 'file-name': self.FILENAME}

        self.assertEqual(result_inclusion, self.processor.process(inclusion, self.FILENAME))
