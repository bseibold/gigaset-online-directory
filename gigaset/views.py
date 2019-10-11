#!/usr/bin/env python3

"""View for the web app"""

import io
import xml.etree.ElementTree as ET
from flask import Response, request, render_template, abort
from gigaset import app, Gigaset


@app.route('/')
def index():
    """Provide a small info page for browers"""
    return render_template('index.html')


@app.route('/search')
def search():
    """Search function for Gigaset base stations"""

    if not ('command', 'get_list') in request.args.items():
        abort(501)

    results = Gigaset.search(**request.args)

    first = int(request.args.get('first', '1'))
    count = int(request.args.get('count', '16'))
    limit = int(request.args.get('limit', '2048'))

    view = results[first - 1: first - 1 + count]
    view = view[:limit]

    root = ET.Element('list')
    root.attrib['response'] = 'get_list'
    root.attrib['type'] = 'pb'
    root.attrib['total'] = str(len(results))

    if view:
        root.attrib['first'] = str(first)
        root.attrib['last'] = str(len(results))

        for entry in view:
            xml_entry = ET.SubElement(root, 'entry')
            for param in entry:
                xml_x = ET.SubElement(xml_entry, param)
                xml_x.text = entry[param]

    tree = ET.ElementTree(root)
    byteio = io.BytesIO()
    tree.write(byteio, xml_declaration=True)
    return Response(byteio.getvalue(), mimetype='text/xml')
