import re

__all__ = ['indent']

class TokenMeta(type):

    _token_classes = {}

    def __new__(cls, name, bases, attrs):
        kls = type.__new__(cls, name, bases, attrs)
        cls._token_classes[name] = kls
        return kls
        
    @classmethod
    def getclass(cls, name):
        return cls._token_classes[name]

# need to proceed that way for Python 2/3 compatility:
TokenBase = TokenMeta('TokenBase', (object,), {}) 
    
class Token(TokenBase):
    regex = None
    
    def __init__(self, groupdict):
        self.content = groupdict[self.__class__.__name__]
        
class Text(Token):
    regex = '[^<>]+'
    def __init__(self, *args, **kwargs):
        super(Text, self).__init__(*args, **kwargs)
        self._isblank = None
        
    @property
    def isblank(self):
        if self._isblank is None:
            self._isblank = not self.content.strip()
        return self._isblank
    
class Comment(Token):
    regex = r'<!--((?!-->).)*.?-->'

class CData(Token):
    regex = r'<!\[CDATA\[((?!\]\]>).*).?\]\]>'
    
class Doctype(Token):
    regex = r'''<!DOCTYPE(\s+([^<>"']+|"[^"]*"|'[^']*'))*>'''
    
_open_tag_start = r'''
    <\s*
        (?P<{tag_name_key}>{tag_name_rgx})
        (\s+[^/><"=\s]+     # attribute
            (\s*=\s*
                (
                    [^/><"=\s]+ |    # unquoted attribute value
                    ("[^"]*") |    # " quoted attribute value
                    ('[^']*')      # ' quoted attribute value
                )
            )?  # the attribute value is optional (we're forgiving)
        )*
    \s*'''

class Script(Token):
    _end_script = r'<\s*/\s*script\s*>'
    
    regex = _open_tag_start.format(
        tag_name_key = 'script_ignore',
        tag_name_rgx = 'script',
    ) + r'>((?!({end_script})).)*.?{end_script}'.format(
        end_script = _end_script
    )
    
class Style(Token):
    _end_style = r'<\s*/\s*style\s*>'
    
    regex = _open_tag_start.format(
        tag_name_key = 'style_ignore',
        tag_name_rgx = 'style',
    ) + r'>((?!({end_style})).)*.?{end_style}'.format(
        end_style = _end_style
    )

class XMLDeclaration(Token):
    regex = _open_tag_start.format(
        tag_name_key = 'xmldecl_ignore',
        tag_name_rgx = r'\?\s*xml'
    ) + r'\?\s*>'

class NamedTagTokenMeta(TokenMeta):
    def __new__(cls, name, bases, attrs):
        kls = TokenMeta.__new__(cls, name, bases, attrs)
        if name not in('NamedTagTokenBase', 'NamedTagToken'):
            kls.tag_name_key = 'tag_name_%s' % name
            kls.regex = kls.regex_template.format(
                tag_name_key = kls.tag_name_key,
                tag_name_rgx = kls.tag_name_rgx
            )
        return kls

# need to proceed that way for Python 2/3 compatility
NamedTagTokenBase = NamedTagTokenMeta(
    'NamedTagTokenBase',
    (Token,),
    {'tag_name_rgx': r'[^/><"\s]+'}
)

class NamedTagToken(NamedTagTokenBase):
    def __init__(self, groupdict):
        super(NamedTagToken, self).__init__(groupdict)
        self.tag_name = groupdict[self.__class__.tag_name_key]
        
class OpenTag(NamedTagToken):
    regex_template = _open_tag_start + '>'
    
class SelfTag(NamedTagToken): # a self closing tag
    regex_template = _open_tag_start + r'/\s*>'
    
class CloseTag(NamedTagToken):
    regex_template = r'<\s*/(?P<{tag_name_key}>{tag_name_rgx})(\s[^/><"]*)?>'

class XMLTokenError(Exception):
        pass

class Tokenizer(object):
        
    def __init__(self, token_classes):
        self.token_classes = token_classes
        self.token_names = [kls.__name__ for kls in token_classes]
        self.get_token = None
        
    def _compile_regex(self):
        self.get_token = re.compile(
            '|'.join(
                '(?P<%s>%s)' % (klass.__name__, klass.regex) for klass in self.token_classes
            ),
            re.X | re.I | re.S
        ).match
        
    def tokenize(self, string):
        if not self.get_token:
            self._compile_regex()
        result = []
        append = result.append
        while string:
            mobj = self.get_token(string)
            if mobj:
                groupdict = mobj.groupdict()
                class_name = next(name for name in self.token_names if groupdict[name])
                token = TokenMeta.getclass(class_name)(groupdict)
                append(token)
                string = string[len(token.content):]
            else:
                raise XMLTokenError("Unrecognized XML token near %s" % repr(string[:100]))
            
        return result
        
tokenize = Tokenizer(
    (Text, Comment, CData, Doctype, XMLDeclaration, Script, Style, OpenTag, SelfTag, CloseTag)
).tokenize

class TagMatcher(object):

    class SameNameMatcher(object):
        def __init__(self):
            self.unmatched_open = []
            self.matched = {}
            
        def sigclose(self, i):
            if self.unmatched_open:
                open_tag = self.unmatched_open.pop()
                self.matched[open_tag] = i
                self.matched[i] = open_tag
                return open_tag
            else:
                return None
                
        def sigopen(self, i):
            self.unmatched_open.append(i)
                   
    def __init__(self, token_list, blank_is_text = False):
        self.token_list = token_list
        self.name_matchers = {}
        self.direct_text_parents = set()
        
        for i in range(len(token_list)):
            token = token_list[i]
            tpe = type(token)
            if tpe is OpenTag:
                self._get_name_matcher(token.tag_name).sigopen(i)
            elif tpe is CloseTag:
                self._get_name_matcher(token.tag_name).sigclose(i)
        
        # TODO move this somewhere else
        current_nodes = []
        for i in range(len(token_list)):
            token = token_list[i]
            tpe = type(token)
            if tpe is OpenTag and self.ismatched(i):
                current_nodes.append(i)
            elif tpe is CloseTag and self.ismatched(i):
                current_nodes.pop()
            elif tpe is Text and (blank_is_text or not token.isblank):
                if current_nodes:
                    self.direct_text_parents.add(current_nodes[-1])
                        
    def _get_name_matcher(self, tag_name):
        try:
            return self.name_matchers[tag_name]
        except KeyError:
            self.name_matchers[tag_name] = name_matcher = self.__class__.SameNameMatcher()
            return name_matcher
            
    def ismatched(self, i):
        return i in self.name_matchers[self.token_list[i].tag_name].matched
        
    def directly_contains_text(self, i):
        return i in self.direct_text_parents
                
            
def indent(string, indentation = '  ', newline = '\n', indent_text = False, blank_is_text = False):
    """
    takes a string representing a html or xml document and returns
     a well indented version of it
    
    arguments:
    - string: the string to process
    - indentation: the indentation unit (default to two spaces)
    - newline: the string to be use for new lines
      (default to  '\\n', could be set to '\\r\\n' for example)
    - indent_text:
        
        if True, text nodes will be indented:
        
            <p>Hello</p>
            
            would result in
            
            <p>
                hello
            </p>
        
        if False, text nodes won't be indented, and the content
         of any node directly containing text will be unchanged:
         
            <p>Hello</p> will be unchanged
            
            <p><strong>Hello</strong> world!</p> will be unchanged
             since ' world!' is directly contained in the <p> node.
            
            This is the default since that's generally what you want for HTML.
        
    - blank_is_text:
        if False, completely blank texts are ignored. That is the default.
    """ 
    tokens = tokenize(string)
    tag_matcher = TagMatcher(tokens, blank_is_text = blank_is_text)
    ismatched = tag_matcher.ismatched
    directly_contains_text = tag_matcher.directly_contains_text
    result = []
    append = result.append
    level = 0
    sameline = 0
    was_just_opened = False
    tag_appeared = False
    def _indent():
        if tag_appeared:
            append(newline)
        for i in range(level):
            append(indentation)
    for i,token in enumerate(tokens):
        tpe = type(token)
        if tpe is Text:
            if blank_is_text or not token.isblank:
                if not sameline:
                    _indent()
                append(token.content)
                was_just_opened = False
        elif tpe is OpenTag and ismatched(i):
            was_just_opened = True
            if sameline:
                sameline += 1
            else:
                _indent()
            if not indent_text and directly_contains_text(i):
                sameline = sameline or 1
            append(token.content)
            level += 1
            tag_appeared = True
        elif tpe is CloseTag and ismatched(i):
            level -= 1
            tag_appeared = True
            if sameline:
                sameline -= 1
            elif not was_just_opened:
                _indent()
            append(token.content)
            was_just_opened = False
        else:
            if not sameline:
                _indent()
            append(token.content)
            was_just_opened = False
            tag_appeared = True
    return ''.join(result)
    
if __name__ == '__main__':
    import sys
    print(indent(sys.stdin.read()))

