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
</body>""",
            """
            <html>
            <body>
            <p><strong>Important:</strong> the content of nodes that directly contain text should be preserved.</p>
            <div>
            <p>But the content of nodes that don't (like the parent div here) should be indented.</p>
            </div>
            </body>
            </html>
""": """\
<html>
    <body>
        <p><strong>Important:</strong> the content of nodes that directly contain text should be preserved.</p>
        <div>
            <p>But the content of nodes that don't (like the parent div here) should be indented.</p>
        </div>
    </body>
</html>""",
            '<p>Hello <i>world</i>!</p>': "<p>Hello <i>world</i>!</p>",
            
            '<?xml version="1.0" encoding="utf-8"?><a><b/><b/></a>': '''\
<?xml version="1.0" encoding="utf-8"?>
<a>
    <b/>
    <b/>
</a>'''
        }
        
        self.targets_indent_text = { '<p>Hello <i>world</i>!</p>': """\
<p>
    Hello 
    <i>
        world
    </i>
    !
</p>"""
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
            
    def test_indent_text_option(self):
        for source, target in self.targets_indent_text.items():
            self.assertEqual(
                indent(source, indentation = "    ", indent_text = True),
                target
            )
                


if __name__ == '__main__':
    unittest.main()
