#!/usr/bin/env python3
import argparse
import sys

import yaml

from markdown import output_markdown
from parse import parse_pfsense
from pfsense import PfSenseDocument
from progress import Animation


def output_yaml(doc, stream):
    yaml.safe_dump(doc.data, stream)

OUTPUT_FORMATS = {
    'yaml': output_yaml,
    'md': output_markdown,
}

def get_output_func(args):
    return OUTPUT_FORMATS.get(args.output_format, output_yaml)

def get_progress_animation(args):
    return Animation(args.quiet or args.output_path == '-')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", dest="quiet", action="store_const", const=True, default=False, help="Hide progress messages")
    parser.add_argument("-i", dest="input_path", help="XML input path", required=True)
    parser.add_argument("-o", dest="output_path", help="Output path", default="-")
    parser.add_argument("-f", dest="output_format", help="Output format", default="yaml", choices=OUTPUT_FORMATS.keys())
    return parser.parse_args()

def step_parse(args, doc):
    if not args.quiet:
        print('\u268b Parsing "{}" ...'.format(args.input_path), file=sys.stderr)
    with get_progress_animation(args):
        parse_pfsense(args.input_path, doc)
    if not args.quiet:
        print('\u268d Successfully parsed pfSense config version {}.'.format(doc.pfsense.version), file=sys.stderr)

def step_stdout(args, doc, output_func):
    if not args.quiet:
        print('\u2631 Outputting to stdout ...', file=sys.stderr)
    with get_progress_animation(args):
        output_file = sys.stdout
        output_func(doc, output_file)
    if not args.quiet:
        print('\u2630 Successfully outputted pfSense config as {}.'.format(args.output_format), file=sys.stderr)

def step_file(args, doc, output_func):
    if not args.quiet:
        print('\u2631 Outputting to "{}" ...'.format(args.output_path), file=sys.stderr)
    with get_progress_animation(args):
        with open(args.output_path, 'w+') as output_file:
            output_func(doc, output_file)
    if not args.quiet:
        print('\u2630 Successfully outputted pfSense config as {}.'.format(args.output_format), file=sys.stderr)

def main():
    args = parse_args()
    doc = PfSenseDocument()
    output_func = get_output_func(args)

    step_parse(args, doc)
    if args.output_path == '-':
        step_stdout(args, doc, output_func)
    else:
        step_file(args, doc, output_func)

if __name__ == '__main__':
    main()
