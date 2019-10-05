#!/usr/bin/env python3

import io
from flask import Response, request, render_template, abort
import concurrent.futures
import xml.etree.ElementTree as ET
from gigaset import app, Gigaset

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    if not ('command', 'get_list') in request.args.items():
        abort(501)

    results = Gigaset.search(**request.args)

    first = int(request.args.get('first', '1'))
    count = int(request.args.get('count', '16'))
    limit = int(request.args.get('limit', '2048'))

    view = results[first + 1 : first + 1 + count]

    root = ET.Element('list')
    root.attrib['response'] = 'get_list'
    root.attrib['type'] = 'pb'
    root.attrib['total'] = str(len(results))

    if results:
        root.attrib['first'] = str(first)
        root.attrib['last'] = str(len(results))

        for entry in results:
            xml_entry = ET.SubElement(root, 'entry')
            for x in entry:
                xml_x = ET.SubElement(xml_entry, x)
                xml_x.text = entry[x]

    tree = ET.ElementTree(root)
    f = io.BytesIO()
    tree.write(f, xml_declaration=True)
    return Response(f.getvalue(), mimetype='text/xml')
