import unittest
from juliet import fileParser

class fileParserTest(unittest.TestCase):

    def test_parsingValidFile1(self):
        """ Make sure that process() returns the excepted result when passing
        simple, valid files."""

        validFile = """---
key: value
whatever: anothervalue
22i: valuewithnumbers5
---

body"""

        result = {"header": "key: value\nwhatever: anothervalue\n22i: valuewithnumbers5", "body": "<p>body</p>"}

        self.assertEqual(result, fileParser.process(validFile, "/whatever/baseurl"))

    def test_parsingValidFile2(self):
        """ Make sure that process() returns the excepted result when passing
        simple, valid files with empty header and body."""

        validFile1 = """---
---

body"""

        validFile2 = """body"""

        result1 = {"header": "", "body": "<p>body</p>"}

        validFile3 = """---

---"""

        result3 = {"header": "", "body": ""}

        validFile4 = """"""

        result4 = {"header": "", "body": ""}

        dummyUrl = "/whatever/baseurl"
        self.assertEqual(result1, fileParser.process(validFile1, dummyUrl))
        self.assertEqual(result1, fileParser.process(validFile2, dummyUrl))
        self.assertEqual(result3, fileParser.process(validFile3, dummyUrl))
        self.assertEqual(result4, fileParser.process(validFile4, dummyUrl))

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

        result1 = {"header": "", "body": """<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file
</pre></div>
</td></tr></table>

<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file
</pre></div>
</td></tr></table>"""}

        dummyUrl = "/whatever/baseurl"
        self.assertEqual(result1, fileParser.process(file1, dummyUrl))

    def test_invalidFile(self):
        """ Make sure that process() returns None if passed file is invalid."""

        invalidFile = """---
key: value

body"""

        self.assertEqual(None, fileParser.process(invalidFile, "/whatever/baseurl"))
