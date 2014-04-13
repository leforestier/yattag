import unittest
from yattag import indent

class TestIndent(unittest.TestCase):

    def setUp(self):
        self.targets = {
            '<p>aaa</p>': '<p>aaa</p>',
            '<html><body><p>1</p><p>2</p></body></html>': """\
<html>
    <body>
        <p>1</p>
        <p>2</p>
    </body>
</html>""",
            '<body><div id="main"><img src="photo1"><img src="photo2"></div></body>': """\
<body>
    <div id="main">
        <img src="photo1">
        <img src="photo2">
    </div>
</body>"""
        }

    def test_indent(self):
        for source, target in self.targets.items():
            self.assertEqual(
                indent(source, indentation = "    "),
                target
            )
        
    def test_idempotent(self):
        for source, target in self.targets.items():
            self.assertEqual(
                indent(source),
                indent(indent(source))
            )


if __name__ == '__main__':
    unittest.main()
