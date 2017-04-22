import unittest
from juliet import FileParser

class fileParserTest(unittest.TestCase):
    def test_process_pygments(self):
        body = """This is a test.
{% highlight shell %}
cat file
{% endhighlight %}"""
        result = """This is a test.
<table class="sourcetable"><tr><td class="linenos"><div class="linenodiv"><pre>1</pre></div></td><td class="code"><div class="source"><pre><span></span>cat file
</pre></div>
</td></tr></table>
"""
        self.assertEqual(result, FileParser.processPygments(body))

if __name__ == '__main__':
    unittest.main()
