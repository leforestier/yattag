__all__ = ['SimpleDoc']

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
        """
        opens a HTML/XML tag for use inside a `with` statement
        the tag is closed when leaving the `with` block
        HTML/XML attributes can be supplied as keyword arguments.
        The values of the keyword arguments are escaped for use as HTML attributes
        (the " character is replace with &quot;)
        
        In order to supply a "class" html attributes, you must supply a `klass` keyword
        argument. This is because `class` is a reserved python keyword so you can't use it
        outside of a class definition.
        
        Example::
        
            with tag('h1', id = 'main-title'):
                text("Hello world!")
                
            # <h1 id="main-title">Hello world!</h1> was appended to the document
        """
        return self.__class__.Tag(self, tag_name, kwargs)

    def block(self, open_delimiter, close_delimiter):
        return self.__class__.Block(self, open_delimiter, close_delimiter)
        
    def text(self, *strgs):
        """
        appends 0 or more strings to the document
        the strings are escaped for use as text in html documents, that is, 
        & becomes &amp;
        < becomes &lt;
        > becomes &gt;
        
        Example::
        
            username = 'Max'
            text('Hello ', username, '!') # appends "Hello Max!" to the current node
            text('16 > 4') # appends "16 &gt; 4" to the current node
        """
        for strg in strgs:
            self._append(html_escape(strg))
        
    def asis(self, *strgs):
        """
        appends 0 or more strings to the documents
        contrary to the `text` method, the strings are appended "as is"
        &, < and > are NOT escaped
        
        Example::
        
            doc.asis('<!DOCTYPE html>') # appends <!DOCTYPE html> to the document
        """
        for strg in strgs:
            self._append(strg)
        
    def nl(self):
        self._append('\n')
        
    def attr(self, **kwargs):
        """
        sets HTML/XML attribute(s) on the current tag
        HTML/XML attributes are supplied as keyword arguments.
        The values of the keyword arguments are escaped for use as HTML attributes
        (the " character is replaced with &quot;)
        Note that, instead, you can set html/xml attributes by passing them as
        keyword arguments to the `tag` method.
        
        Example::
            
            with tag('h1'):
                text('Welcome!')
                doc.attr(id = 'welcome-message', klass = 'main-title')
            
            # you get: <h1 id="welcome-message" class="main-title">Welcome!</h1>
        
        """
        
        self.current_tag.attrs.update(kwargs)
        
    def stag(self, tag_name, **kwargs):
        """
        appends a self closing tag to the document
        html/xml attributes can be supplied as keyword arguments.
        The values of the keyword arguments are escaped for use as HTML attributes
        (the " character is replaced with &quot;)
        
        Example::
        
            doc.stag('img', src = '/salmon-plays-piano.jpg')
            # appends <img src="/salmon-plays-piano.jpg /> to the document
        """
        
        if kwargs:
            self._append("<%s %s />" % (
                tag_name,
                dict_to_attrs(kwargs),
            ))
        else:
            self._append("<%s />" % tag_name)
            
    def getvalue(self):
        """
        returns the whole document as a single string
        """
        return ''.join(self.result)
        
    def tagtext(self):
        """
        return a triplet composed of::
            . the document itself
            . its tag method
            . its text method
        
        Example::
        
            doc, tag, text = SimpleDoc().tagtext()
            
            with tag('h1'):
                text('Hello world!')
                
            print(doc.getvalue()) # prints <h1>Hello world!</h1>
        """
            
        return self, self.tag, self.text

    def blockasis(self):
        return self, self.block, self.asis
        

class DocError(Exception):
    pass
          
def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def attr_escape(s):
    return s.replace('"', "&quot;")

def dict_to_attrs(dct):
    try:
        if 'klass' in dct and dct['klass']:
            lst = ['%s="%s"' % (key, arg.replace('"', "&quot;")) for (key, arg) in dct.items() if key != "klass"]
            lst.append('class="%s"' % dct['klass'].replace('"', "&quot;"))
        else:
            lst = ['%s="%s"' % (key, arg.replace('"', "&quot;")) for (key, arg) in dct.items() if arg]
    except AttributeError as e:
        if "'replace'" in str(e):
            raise ValueError("xml/html attributes should be strings. %s" % e)
        else:
            raise
    return ' '.join(lst)

            
        
