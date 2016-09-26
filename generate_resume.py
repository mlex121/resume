#!/usr/bin/env python
from __future__ import print_function

import argparse
import json
import sys
from jinja2 import (
    Environment, FileSystemLoader, TemplateNotFound, TemplateSyntaxError
)


def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return unicode(f.read(), 'utf-8')
    except IOError as e:
        print('Error opening ' + filename + ': ' + str(e),
              file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Generates an HTML resume rendered from the given '
                    'template file and JSON-formatted data.')
    parser.add_argument('template',
                        help='The Jinja2 template file to be rendered.')
    parser.add_argument('data',
                        help='The JSON-formatted data to be passed to the '
                             'template renderer.')
    parser.add_argument('-o', '--outfile',
                        help='The destination file to write the resume to. If '
                             'not specified, writes the result to standard '
                             'output.')
    parser.add_argument('-c', '--css',
                        help='The primary CSS file for the document.')
    parser.add_argument('-f', '--font-css',
                        help='The font CSS file for the document.')
    parser.add_argument('-p', '--print-css',
                        help='The print media CSS file for the document.')
    parser.add_argument('-i', '--inline-css',
                        action='store_true',
                        dest='use_inline_css',
                        help='If specified, generate the resume with the CSS '
                             'inserted inline (within <style> tags). Defaults '
                             'to False.')
    parser.add_argument('-l', '--cover-letter',
                        help='A cover letter to be inserted before the resume.'
                        )

    args = parser.parse_args()
    env = Environment(loader=FileSystemLoader('.'),
                      trim_blocks=True,
                      lstrip_blocks=True)

    # Template
    try:
        template = env.get_template(args.template)
    except TemplateNotFound as e:
        print('Error loading template ' + args.template + ', not found',
              file=sys.stderr)
        sys.exit(1)
    except TemplateSyntaxError as e:
        print('Syntax error in template ' + args.template + ' on line '
              + str(e.lineno) + ': ' + e.message, file=sys.stderr)
        sys.exit(1)

    # JSON data
    try:
        with open(args.data, 'r') as f:
            context = json.loads(f.read())
    except IOError as e:
        print('Error opening ' + args.data + ': ' + str(e), file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print('Error parsing JSON file ' + args.data + ': ' + str(e),
              file=sys.stderr)
        sys.exit(1)

    # CSS files
    if args.use_inline_css:
        context['use_inline_css'] = True
        if args.css:
            context['css'] = read_file(args.css)
        if args.font_css:
            context['font_css'] = read_file(args.font_css)
        if args.print_css:
            context['print_css'] = read_file(args.print_css)
    else:
        if args.css:
            context['css_file'] = args.css
        if args.font_css:
            context['font_css_file'] = args.font_css
        if args.print_css:
            context['print_css_file'] = args.print_css

    # Cover letter
    if args.cover_letter:
        context['cover_letter'] = read_file(args.cover_letter)

    # Render template
    try:
        result = template.render(**context)
    except UnicodeError as e:
        print('Error rendering: ' + str(e), file=sys.stderr)
        sys.exit(1)

    # Write output
    if args.outfile:
        try:
            with open(args.outfile, 'w') as f:
                f.write(result.encode('utf-8'))
        except IOError as e:
            print('Error writing to file ' + args.outfile + ': ' + str(e),
                  file=sys.stderr)
    else:
        print(result)


if __name__ == '__main__':
    main()
