import os,sys,inspect
from collections import Counter,OrderedDict
from yattag import Doc,indent
def get_table_html(header, rows, row_names=None):
    def add_header(doc, header):
        with doc.tag('tr'):
            for value in header:
                doc.line('th', value)

    def add_row(doc, values, row_name=None):
        with doc.tag('tr'):
            if row_name is not None:
                doc.line('th', row_name)
            for value in values:
                doc.line('td', value)

    doc = Doc()
    if row_names is not None:
        header.insert(0, '')
    else:
        row_names = [None] * len(rows)
    with doc.tag('table', klass='table table-bordered table-responsive table-striped table-hover'):
        with doc.tag('thead', klass='thead-light'):
            add_header(doc, header)
        with doc.tag('tbody'):
            for row, row_name in zip(rows, row_names):
                add_row(doc, [round(val, 2) for val in row], row_name)
    return indent(doc.getvalue())
doc, tag, text, line = Doc().ttl()

doc.asis('<!DOCTYPE html>')

with tag('html'):
    with tag("head"):

        line("link", '''rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"
    integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous"''')
    with tag('body'): 
        doc.asis(get_table_html(["header1","header2","header3"],[[1,2,3],[1.0,2.0,3]],["name1","name2","name3"]))
if __name__ == "__main__":
    print(indent(doc.getvalue()))
    with open("yattag_test.html", 'w', encoding='utf-8') as file:
        file.write(indent(doc.getvalue()))