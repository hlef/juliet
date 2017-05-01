import unittest
from juliet import fileParser

class fileParserTest(unittest.TestCase):

    FILENAME = "filename"

    def test_parsingValidFile1(self):
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

        self.assertEqual(result, fileParser.process(validFile, self.FILENAME, "/baseurl"))

    def test_parsingValidFile2(self):
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

        dummyUrl = "/url"
        self.assertEqual(result1, fileParser.process(validFile1, self.FILENAME, dummyUrl))
        self.assertEqual(result1, fileParser.process(validFile2, self.FILENAME, dummyUrl))
        self.assertEqual(result3, fileParser.process(validFile3, self.FILENAME, dummyUrl))
        self.assertEqual(result4, fileParser.process(validFile4, self.FILENAME, dummyUrl))

    def test_pygments(self):
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

        self.assertEqual(result1, fileParser.process(file1, self.FILENAME, "/url"))

    def test_invalidFile(self):
        """ Make sure that process() returns None if passed file is invalid."""

        invalidFile = """---
key: value

body"""

        self.assertRaises(ValueError, fileParser.process, invalidFile, self.FILENAME, "/url")
