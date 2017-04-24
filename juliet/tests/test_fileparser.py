import unittest
from juliet import FileParser

class fileParserTest(unittest.TestCase):
    def test_process_pygments1(self):
        """ Make sure that processPygments() is working well with simple
        entries that declare a single highlight statement.

        Also make sure that the highlight statement is recognized even if spaces
        are missing or duplicated. """

        # No additional or missing spaces
        body1 = """This is a test.
{% highlight shell %}
cat file
{% endhighlight %}"""

        # Missing and additional spaces
        body2 = """This is a test.
{%  highlight shell%}
cat file
{%endhighlight  %}"""

        result = """This is a test.
<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file
</pre></div>
</td></tr></table>
"""
        self.assertEqual(result, FileParser.processPygments(body1))
        self.assertEqual(result, FileParser.processPygments(body2))

    def test_process_pygments2(self):
        """ Make sure that processPygments() is working well with more complex
        entries that declare multiple highlight statements."""

        body = """This is a test.
{% highlight shell %}
cat file
{% endhighlight  %}
{%highlight shell %}
cat file
{%endhighlight%}"""

        result = """This is a test.
<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file
</pre></div>
</td></tr></table>
<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file
</pre></div>
</td></tr></table>
"""
        self.assertEqual(result, FileParser.processPygments(body))

    def test_parsingValidFile1(self):
        """ Make sure that getParsed() returns the excepted result when passing
        simple, valid files."""

        validFile = """---
key: value
whatever: anothervalue
22i: valuewithnumbers5
---

body"""

        result = {"header": "key: value\nwhatever: anothervalue\n22i: valuewithnumbers5\n", "body": "<p>body</p>"}

        self.assertEqual(result, FileParser.getParsed(validFile, "/whatever/baseurl"))

    def test_parsingValidFile2(self):
        """ Make sure that getParsed() returns the excepted result when passing
        simple, valid files with empty header and body."""

        validFile1 = """---
---

body"""

        validFile2 = """body"""

        result1 = {"header": "", "body": "<p>body</p>"}

        validFile3 = """---

---"""

        result3 = {"header": "\n", "body": ""}

        self.assertEqual(result1, FileParser.getParsed(validFile1, "/whatever/baseurl"))
        self.assertEqual(result1, FileParser.getParsed(validFile2, "/whatever/baseurl"))
        self.assertEqual(result3, FileParser.getParsed(validFile3, "/whatever/baseurl"))

    def test_invalidFile(self):
        """ Make sure that getParsed() returns None if passed file is invalid."""

        invalidFile = """---
key: value

body"""

        self.assertEqual(None, FileParser.getParsed(invalidFile, "/whatever/baseurl"))
