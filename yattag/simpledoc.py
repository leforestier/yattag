__all__ = ['SimpleDoc']

class DocError(Exception):
    pass
          
def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def attr_escape(s):
    return s.replace('"', "&quot;")

def dict_to_attrs(dct):
    try:
        if 'klass' in dct:
            lst = ['%s="%s"' % (key, arg.replace('"', "&quot;")) for (key, arg) in dct.items() if key != "klass"]
            lst.append('class="%s"' % dct['klass'].replace('"', "&quot;"))
        else:
            lst = ['%s="%s"' % (key, arg.replace('"', "&quot;")) for (key, arg) in dct.items()]
    except AttributeError as e:
        if "'replace'" in str(e):
            raise ValueError("xml/html attributes should be strings. %s" % e)
        else:
            raise
    return ' '.join(lst)
    
class SimpleDoc(object):

    """
    class generating xml/html documents using context managers
    
    doc, tag, text = SimpleDoc().tagtext()

    with tag('html'):
        with tag('body', id = 'hello'):
            with tag('h1'):
                text('Hello world!')

    print(doc.getvalue())
    """
            
    class Tag(object):
        def __init__(self, doc, name, attrs): # name is the tag name (ex: 'div')
            
            self.doc = doc
            self.name = name
            self.attrs = attrs
            
        def __enter__(self):
            self.parent_tag = self.doc.current_tag
            self.doc.current_tag = self
            self.position = len(self.doc.result)
            self.doc._append('')
            
        def __exit__(self, tpe, value, traceback):
            if value is None:
                if self.attrs:
                    self.doc.result[self.position] = "<%s %s>" % (
                        self.name,
                        dict_to_attrs(self.attrs),
                    )
                else:
                    self.doc.result[self.position] = "<%s>" % self.name
                self.doc._append("</%s>" % self.name)
                self.doc.current_tag = self.parent_tag

    class Block(object):
        def __init__(self, doc, open_delimiter, close_delimiter = None):
            self.doc = doc
            self.open_delimiter = open_delimiter
            if close_delimiter is None:
                if open_delimiter == '{':
                    self.close_delimiter = '}'
                elif open_delimiter == '(':
                    self.close_delimiter = ')'
                elif open_delimiter == '/*':
                    self.close_delimiter = '*/'
                else:
                    self.close_delimiter = open_delimiter

        def __enter__(self):
            self.doc._append(self.open_delimiter)

        def __exit__(self, tpe, value, traceback):
            if value is None:
                self.doc._append(self.close_delimiter)
         
    class DocumentRoot(object):
        def __getattr__(self, item):
            raise DocError("DocumentRoot here. You can't access anything here.")
        
    def __init__(self):
        self.result = []
        self.current_tag = self.__class__.DocumentRoot()
        self._append = self.result.append
        
    def tag(self, tag_name, **kwargs): 
        return self.__class__.Tag(self, tag_name, kwargs)

    def block(self, open_delimiter, close_delimiter):
        return self.__class__.Block(self, open_delimiter, close_delimiter)
        
    def text(self, strg):
        self._append(html_escape(strg))
        
    def asis(self, strg):
        self._append(strg)
        
    def nl(self):
        self._append('\n')
        
    def attr(self, **kwargs):
        self.current_tag.attrs.update(kwargs)
        
    def stag(self, tag_name, **kwargs):
        if kwargs:
            self._append("<%s %s />" % (
                tag_name,
                dict_to_attrs(kwargs),
            ))
        else:
            self._append("<%s />" % tag_name)
            
    def getvalue(self):
        return ''.join(self.result)
        
    def tagtext(self):
        return self, self.tag, self.text

    def blockasis(self):
        return self, self.block, self.asis

            
        
