#!/usr/bin/env python3
import argparse
import io
from pprint import pprint
from xml.sax import ContentHandler

from defusedxml.sax import parse

from pfsense import PfSenseDocument
from util import DataList


class PfSenseContentHandler(ContentHandler):
    def __init__(self, document):
        self.document = document
        self.stack = []

    def startDocument(self):
        stack_chars = io.StringIO()
        stack_frame = (self.document, None, 'element', stack_chars)
        self.stack.append(stack_frame)

    def startElement(self, name, attrs):
        attr_name = name.replace('-', '_')
        cur, _, _, _ = self.stack[-1]

        klass = None
        klass_type = 'unknown'
        klass_lookup = '_%s' % attr_name
        klass = getattr(cur, klass_lookup, None)
        if isinstance(klass, list):
            klass = klass[0]
            klass_type = 'element'
        elif not klass is None:
            klass_type = 'attribute'
        if not klass is None:
            new = klass(cur)
        else:
            new = None

        stack_chars = io.StringIO()
        stack_frame = (new, name, klass_type, stack_chars)
        self.stack.append(stack_frame)

    def characters(self, content):
        cur, _, _, stack_chars = self.stack[-1]
        if not stack_chars is None:
            stack_chars.write(content)
            if not cur is None:
                cur(stack_chars.getvalue())

    def endElement(self, name):
        if name != self.stack[-1][1]:
            raise RuntimeError("Invalid stack order")

        attr_name = name.replace('-', '_')
        cur, cur_name, cur_type, _ = self.stack.pop()
        old, _, _, _ = self.stack[-1]

        if cur_type == 'element':
            elements = getattr(old, attr_name, DataList())
            elements.append(cur)
            setattr(old, attr_name, elements)

        elif cur_type == 'attribute':
            setattr(old, attr_name, cur)

    def endDocument(self):
        if self.stack[-1][0] != self.document:
            raise RuntimeError("Pending stack elements")

def parse_pfsense(input_path, document):
    handler = PfSenseContentHandler(document)
    with open(input_path, 'rb') as input_file:
        parse(input_file, handler)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="XML input path")
    return parser.parse_args()

def main():
    args = parse_args()
    doc = PfSenseDocument()
    parse_pfsense(args.input_path, doc)
    pprint(doc)

if __name__ == '__main__':
    main()
