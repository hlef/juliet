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
