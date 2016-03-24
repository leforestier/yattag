.. image:: https://travis-ci.org/leforestier/yattag.svg
    :target: https://travis-ci.org/leforestier/yattag

Why use a template engine when you can generate HTML or XML documents with Python in a very readable way?

( full tutorial on yattag.org_ )

Basic example
-------------

Nested html tags, no need to close tags.

.. code:: python

    from yattag import Doc

    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('body', id = 'hello'):
            with tag('h1'):
                text('Hello world!')

    print(doc.getvalue())

    
Html form rendering
-------------------

Yattag can fill your HTML forms with default values and error messages.
Pass a ``defaults`` dictionnary of default values, and an ``errors`` dictionnary of error messages to the ``Doc`` constructor.
Then, use the special ``input``, ``textarea``, ``select``, ``option`` methods when generating your documents.


Example with default values
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from yattag import Doc

    doc, tag, text = Doc(
        defaults = {'ingredient': ['chocolate', 'coffee']}
    ).tagtext()

    with tag('form', action = ""):
        with tag('label'):
            text("Select one or more ingredients")
        with doc.select(name = 'ingredient', multiple = "multiple"):
            for value, description in (
                ("chocolate", "Dark chocolate"),
                ("almonds", "Roasted almonds"),
                ("honey", "Acacia honey"),
                ("coffee", "Ethiopian coffee")
            ):
                with doc.option(value = value):
                    text(description) 
        doc.stag('input', type = "submit", value = "Validate")

    print(doc.getvalue())

Example with default values and errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from yattag import Doc

    doc, tag, text = Doc(
        defaults = {
            'title': 'Untitled',
            'contact_message': 'You just won the lottery!'
        },
        errors = {
            'contact_message': 'Your message looks like spam.'
        }
    ).tagtext()

    with tag('h1'):
        text('Contact form')
    with tag('form', action = ""):
        doc.input(name = 'title', type = 'text')
        with doc.textarea(name = 'contact_message'):
            pass
        doc.stag('input', type = 'submit', value = 'Send my message')

    print(doc.getvalue())
    
Full tutorial on yattag.org_

GitHub repo: https://github.com/leforestier/yattag

.. _yattag.org: http://www.yattag.org
    

