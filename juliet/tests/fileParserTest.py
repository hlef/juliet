import unittest

from juliet import FileParser

class fileParserTest(unittest.Testcase):
    def test_process_pygments(self):
        body = """This is a test.
\{% highlight shell %\}
cat file
\{% endhighlight %\}"""
        result = """This is a test.
\{% highlight shell %\}
cat file
\{% endhighlight %\}"""
        print(FileParser.processPygments(body))
        unittest.assertEquals(result, FileParser.processPygments(body))

if __name__ == '__main__':
    unittest.main()
