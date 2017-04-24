import unittest
from juliet import FileParser

class fileParserTest(unittest.TestCase):
    def test_process_pygments1(self):
        """ Test that processPygments() is working well with simple entries that
        declare a single highlight statement.

        Also make sure that the highlight statement is recognized even if spaces
        are missing or duplicated. """

        body1 = """This is a test.
{% highlight shell %}
cat file
{% endhighlight %}"""
        body2 = """This is a test.
{%highlight shell%}
cat file
{%endhighlight%}"""
        body3 = """This is a test.
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
        self.assertEqual(result, FileParser.processPygments(body3))

    def test_process_pygments2(self):
        """ Test that processPygments() is working well with entries that
        declare multiple highlight statements."""

        body1 = """This is a test.
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
        self.assertEqual(result, FileParser.processPygments(body1))

if __name__ == '__main__':
    unittest.main()
