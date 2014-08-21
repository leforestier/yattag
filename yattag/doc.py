from yattag.simpledoc import dict_to_attrs, html_escape, attr_escape, SimpleDoc, DocError

try:
    range = xrange  # for Python 2/3 compatibility
except NameError:
    pass

__all__ = ['Doc']

class SimpleInput(object):

    """
    class representing text inputs, password inputs, hidden inputs etc...
    """
    
    def __init__(self, name, tpe, **kwargs):
        self.name = name
        self.tpe = tpe
        self.attrs = kwargs
        
    def render(self, defaults, errors, error_wrapper):
        lst = []
        attrs = dict(self.attrs)
        error = errors and self.name in errors
        if error:
            if 'klass' in attrs:
                attrs['klass'] = attrs['klass'] + " error"
            else:
                attrs['klass'] = "error"
            lst.append(error_wrapper[0])
            lst.append(html_escape(errors[self.name]))
            lst.append(error_wrapper[1])
                
        if self.name in defaults:
            attrs['value'] = str(defaults[self.name])
        attrs['name'] = self.name
        lst.append('<input type="%s" %s />' % (self.tpe, dict_to_attrs(attrs)))
        
        return ''.join(lst)
        

class CheckableInput(object):
    tpe = 'checkbox'

    def __init__(self, name, **kwargs):
        self.name = name
        self.rank = 0
        self.attrs = kwargs
        
    def setrank(self, n):
        self.rank = n
    
    def render(self, defaults, errors, error_wrapper):
        lst = []
        attrs = dict(self.attrs)
        if self.rank == 0:
            if errors:
                if self.name in errors:
                    lst.append(error_wrapper[0])
                    lst.append(html_escape(errors[self.name]))
                    lst.append(error_wrapper[1])
                    if 'klass' not in attrs:
                        attrs['klass'] = "error"
        
        if self.name in defaults and 'value' in self.attrs and defaults[self.name] == self.attrs['value']:
            attrs['checked'] = 'checked'
                
        attrs['name'] = self.name
        
        lst.append('<input type="%s" %s />' % (self.__class__.tpe, dict_to_attrs(attrs)))

        return ''.join(lst)
        

class CheckboxInput(CheckableInput):
    pass
    
class RadioInput(CheckableInput):
    tpe = 'radio'
    

def groupclass(inputclass):

    class InputGroup(object):

        def __init__(self, name):
            self.name = name
            self.n_items = 0
            
        def input(self, **kwargs):
            input_instance = inputclass(self.name, **kwargs)
            input_instance.setrank(self.n_items)
            self.n_items += 1
            return input_instance

    return InputGroup

class ContainerTag(object):

    tag_name = 'textarea' 

    def __init__(self, name, **kwargs):
        self.name = name
        self.attrs = kwargs
        
    def render(self, defaults, errors, error_wrapper, inner_content = ''):
        lst = []
        attrs = dict(self.attrs)
        if errors:
            if self.name in errors:
                lst.append(error_wrapper[0])
                lst.append(html_escape(errors[self.name]))
                lst.append(error_wrapper[1])
            if 'klass' not in attrs:
                attrs['klass'] = "error"
        attrs['name'] = self.name

        lst.append('<%s %s>' % (self.__class__.tag_name, dict_to_attrs(attrs)))
        if self.name in defaults:
            lst.append(html_escape(str(defaults[self.name])))
        else:
            lst.append(inner_content)
        
        lst.append('</%s>' % self.__class__.tag_name)

        return ''.join(lst)

class Textarea(ContainerTag):
    pass

class Select(ContainerTag):
    tag_name = 'select'


class Option(object):
    def __init__(self, name, multiple, value, **kwargs):
        self.name = name
        self.multiple = multiple
        self.value = value
        self.attrs = kwargs

    def render(self, defaults, errors, inner_content):
        selected = ''        
        if self.name in defaults:
            if self.multiple:
                if self.value in defaults[self.name]:
                    selected = True
            else:
                if self.value == defaults[self.name]:
                    selected = True
        lst = ['<option value="', attr_escape(self.value), '"']
        if selected:
            lst.append(' selected="selected"')
        if self.attrs:
            lst.append(' ')
            lst.append(dict_to_attrs(self.attrs))
        lst.append('>')
        lst.append(inner_content)
        lst.append('</option>')
        return ''.join(lst)
    
class Doc(SimpleDoc):
    """
    The Doc class extends the SimpleDoc class with form rendering capabilities. 
    Pass default values or errors as dictionnaries to the Doc constructor, and 
    use the `input`, `textarea`, `select`, `option` methods
    to append form elements to the document.
    """
    
    SimpleInput = SimpleInput
    CheckboxInput = CheckboxInput
    RadioInput = RadioInput
    Textarea = Textarea
    Select = Select
    Option = Option
    
    class TextareaTag(object):
        def __init__(self, doc, name, attrs):
            # name is the name attribute of the textarea, ex: 'contact_message'
            # for <textarea name="contact_message">
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
                inner_content = ''.join(self.doc.result[self.position+1:])
                del self.doc.result[self.position+1:]              
                rendered_textarea = self.doc.__class__.Textarea(self.name, **self.attrs).render(
                    defaults = self.doc.defaults,
                    errors = self.doc.errors,
                    inner_content = inner_content,
                    error_wrapper = self.doc.error_wrapper
                )
                self.doc.result[self.position] = rendered_textarea
                self.doc.current_tag = self.parent_tag
                
    
    class SelectTag(object):
        def __init__(self, doc, name, attrs):
            # name is the name attribute of the select, ex: 'color'
            # for <select name="color">
            self.doc = doc
            self.name = name
            self.attrs = attrs
            self.multiple = bool(attrs.get('multiple'))
            self.old_current_select = None
                
        def __enter__(self):
            self.parent_tag = self.doc.current_tag
            self.doc.current_tag = self
            self.position = len(self.doc.result)
            self.doc._append('')
            self.old_current_select = self.doc.current_select
            self.doc.current_select = self
            
        def __exit__(self, tpe, value, traceback):
            if value is None:
                inner_content = ''.join(self.doc.result[self.position+1:])
                del self.doc.result[self.position+1:]
                rendered_select = self.doc.__class__.Select(self.name, **self.attrs).render(
                    defaults = {},  # no defaults for the <select> tag. Defaults are handled by the <option> tags directly.
                    errors = self.doc.errors,
                    inner_content = inner_content,
                    error_wrapper = self.doc.error_wrapper
                )
                self.doc.result[self.position] = rendered_select
                self.doc.current_tag = self.parent_tag  
                self.doc.current_select = self.old_current_select
                

    class OptionTag(object):
        def __init__(self, doc, select, value, attrs):
            self.doc = doc
            self.select = select
            self.attrs = attrs
            self.value = value

        def __enter__(self):
            self.parent_tag = self.doc.current_tag
            self.doc.current_tag = self
            self.position = len(self.doc.result)
            self.doc._append('')
            
        def __exit__(self, tpe, value, traceback):
            if value is None:
                inner_content = ''.join(self.doc.result[self.position+1:])
                del self.doc.result[self.position+1:]
                self.doc.result[self.position] = self.doc.__class__.Option(
                    name = self.select.name,
                    multiple = self.select.multiple,
                    value = self.value, **self.attrs
                ).render(
                    defaults = self.doc.defaults,
                    errors = self.doc.errors,
                    inner_content = inner_content
                )
                self.doc.current_tag = self.parent_tag

    
    def __init__(self, defaults = None, errors = None,\
     error_wrapper = ('<span class="error">', '</span>'), *args, **kwargs):
        """
        creates a Doc instance
        
        defaults::
            optional dictionnary of values used to fill html forms
        errors::
            optional dictionnary of errors used to fill html forms
        
        Example 1::
            doc = Doc()
        
        Example 2::
            doc = Doc(
                defaults = {
                    'beverage': 'coffee',
                    'preferences': ['milk', 'sugar'],
                    'use_discount': True
                },
                errors = {
                    'preferences': "We ran out of milk!"
                }
            )
            
        Note: very often you'll want to call the `tagtext` method just after
        creating a Doc instance. Like this::
        
        doc, tag, text = Doc(defaults = {'color': 'blue'}).tagtext()
        
        This way, you can write `tag` (resp. `text`) in place of `doc.tag`
        (resp. `doc.text`). When writing long html templates or xml documents,
        it's a gain in readability and performance.
        """
                
        super(Doc, self).__init__(*args, **kwargs)
        self.defaults = defaults or {}
        self.errors = errors or {}
        self.error_wrapper = error_wrapper
        self.radios = {}
        self.checkboxes = {}
        self.current_select = None
        self.radio_group_class = groupclass(self.__class__.RadioInput)
        self.checkbox_group_class = groupclass(self.__class__.CheckboxInput)
        self._fields = set()
        self._detached_errors_pos = []
    
     
    def input(self, name, type = 'text', **kwargs):
        self._fields.add(name)
        if type in (
            'text', 'password', 'hidden', 'search', 'email', 'url', 'number',
            'range', 'date', 'datetime', 'datetime-local', 'month', 'week',
            'time', 'color'
        ): 
            self.asis(
                self.__class__.SimpleInput(name, type, **kwargs).render(
                    self.defaults, self.errors, self.error_wrapper
                )
            )
            return
        if type == 'radio':
            if name not in self.radios:
                self.radios[name] = self.radio_group_class(name)
            checkable_group = self.radios[name]
        elif type == 'checkbox':
            if name not in self.checkboxes:
                self.checkboxes[name] = self.checkbox_group_class(name)
            checkable_group = self.checkboxes[name]
        else:
            if type == 'submit':
                raise DocError("Unhandled input type: submit. Use doc.stag('input', type = 'submit', value='whatever') instead.")
            else:
                raise DocError("Unknown input type: %s" % type)
        
        self._append(checkable_group.input(**kwargs).render(self.defaults,self.errors, self.error_wrapper))
        
    def textarea(self, name, **kwargs):
        self._fields.add(name)
        return self.__class__.TextareaTag(self, name, kwargs)
        
    def select(self, name, **kwargs):
        self._fields.add(name)
        return self.__class__.SelectTag(self, name, kwargs)
        
    def option(self, value, **kwargs):
        if self.current_select:
            return self.__class__.OptionTag(self, self.current_select, value, kwargs)
        else:
            raise DocError("No <select> tag opened. Can't put an <option> here.")
            
    def detached_errors(self, render_function = None):
        self._detached_errors_pos.append((len(self.result), render_function or self.error_dict_to_string))
        self.result.append('')
        
    def error_dict_to_string(self, dct):
        if dct:
            doc, tag, text = SimpleDoc().tagtext()
            with tag('ul', klass='error-list'):
                for error in dct.values():
                    with tag('li'):
                        text(error)
            return doc.getvalue()
        else:
            return ''
                        
            
    def getvalue(self):
        """
        returns the whole document as a string
        """
        for position, render_function in self._detached_errors_pos:
            self.result[position] = render_function(
                dict((name, self.errors[name]) for name in self.errors if name not in self._fields)
            )
        return ''.join(self.result)
    
