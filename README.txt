Some examples:

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
    
Html form rendering example with default values
-----------------------------------------------

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
    
Full tutorial on yattag.org_

.. _yattag.org: http://www.yattag.org
    

