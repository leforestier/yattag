from distutils.core import setup

with open('README.txt') as fd:
    long_description = fd.read()

setup(
    name='yattag',
    version='0.8.4',
    packages=['yattag'],
    author = 'Benjamin Le Forestier',
    author_email = 'benjamin@leforestier.org',
    url = 'http://www.yattag.org',
    keywords = ["html", "template", "templating", "xml", "document", "form", "rendering"],
    description = """Library for generating HTML or XML in a pythonic way.\
 Can fill HTML forms with default values and errors. Pure python alternative to\
 html templating languages.""",
    long_description = long_description,
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]  
)
