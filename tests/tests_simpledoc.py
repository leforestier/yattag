import unittest
from yattag import SimpleDoc
import xml.etree.ElementTree as ET

class TestSimpledoc(unittest.TestCase):

    def test_tag(self):
        doc, tag, text = SimpleDoc().tagtext()
        with tag('h1', id = 'main-title'):
            with tag('a', href="/"):
                text("Hello world!")
            with tag('span'):
                text("Hello, CDATA!", cdata=True)
        self.assertEqual(
            doc.getvalue(),
            ''.join([
                '<h1 id="main-title">',
                '<a href="/">Hello world!</a>',
                '<span><![CDATA[Hello, CDATA!]]></span>',
                '</h1>',
            ]),
        )

    def test_attrs(self):
        doc, tag, text = SimpleDoc().tagtext()
        with tag('div', id = 'article'):
            if True:
                doc.attr(klass = 'new')
            else:
                doc.attr(klass = 'old')
            with tag('a', ('data-my-id', '89'), klass='alert'):
                text('hi')
            doc.stag('img', src='squirrel.jpg', klass='animal')

        root = ET.fromstring(doc.getvalue())
        self.assertEqual(root.attrib['class'], "new")
        self.assertEqual(root[0].attrib['class'], "alert")
        self.assertEqual(root[0].attrib['data-my-id'], '89')
        self.assertEqual(root[1].attrib['src'], 'squirrel.jpg')
        self.assertEqual(root[1].attrib['class'], 'animal')
        self.assertRaises(
            KeyError,
            lambda: root[1].attrib['klass']
        )

    def test_attrs_no_value(self):
        doc, tag, text = SimpleDoc().tagtext()
        with tag('paper-button', 'raised'):
            text('I am a fancy button')
        self.assertEqual(
            doc.getvalue(),
            "<paper-button raised>I am a fancy button</paper-button>"
        )


    def test_html_classes(self):
        def class_elems(node):
            return set(node.attrib['class'].split(' '))

        doc, tag, text = SimpleDoc().tagtext()

        with tag('p', klass = 'news'):
            doc.add_class('highlight', 'today')
            doc.discard_class('news')
            doc.toggle_class('active', True)
            with tag('a', href = '/', klass = 'small useless'):
                doc.discard_class('useless')
            with tag('a', href = '/', klass = 'important'):
                doc.discard_class('important')

        root = ET.fromstring(doc.getvalue())
        self.assertEqual(
            class_elems(root),
            set(['highlight', 'today', 'active'])
        )
        self.assertEqual(
            class_elems(root[0]),
            set(['small'])
        )
        self.assertRaises(KeyError, lambda: class_elems(root[1]))

if __name__ == '__main__':
    unittest.main()
