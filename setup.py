from distutils.core import setup

with open('README.rst') as fd:
    long_description = fd.read()

setup(
    name='yattag',
    version='1.16.1',
    package_data={"yattag": ["py.typed"]},
    packages=['yattag'],
    install_requires=[
        'typing;python_version<"3.5"',
    ],
    author = 'Benjamin Le Forestier',
    author_email = 'benjamin@leforestier.org',
    url = 'https://www.yattag.org',
    keywords = ["html", "template", "templating", "xml", "document", "form", "rendering"],
    description = """\
Generate HTML or XML in a pythonic way. Pure python alternative to web template engines.\
Can fill HTML forms with default values and error messages.""",
    long_description = long_description,
    classifiers = [
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
