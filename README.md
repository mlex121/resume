Resume
======

I use this script to generate my resume from JSON-formatted source data and a Jinja2 template.

```
usage: generate_resume.py [-h] [-o OUTFILE] [-c CSS] [-p PRINT_CSS] [-i]
                          [-l COVER_LETTER]
                          template data

Generates an HTML resume rendered from the given template file and JSON-
formatted data.

positional arguments:
  template              The Jinja2 template file to be rendered.
  data                  The JSON-formatted data to be passed to the template
                        renderer.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        The destination file to write the resume to. If not
                        specified, writes the result to standard output.
  -c CSS, --css CSS     The primary CSS file for the document.
  -p PRINT_CSS, --print-css PRINT_CSS
                        The print media CSS file for the document.
  -i, --inline-css      If specified, generate the resume with the CSS
                        inserted inline (within <style> tags). Defaults to
                        False.
  -l COVER_LETTER, --cover-letter COVER_LETTER
                        A cover letter to be inserted before the resume.
```
