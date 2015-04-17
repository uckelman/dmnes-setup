#!/usr/bin/python3 -b

import lxml.html
import subprocess
import sys

from dmnes import *


def make_bib_html(bibtex):
  # FIXME: remove TMPDIR for bibtex2html 1.98+
  cmd = 'TMPDIR=. bibtex2html -nodoc -noheader -nofooter -rawurl -unicode -dl'

  with subprocess.Popen(cmd,
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE) as p:
    out, err = p.communicate(bibtex.encode('utf-8'), timeout=30)
    if p.returncode:
      raise RuntimeError('bibtex2html failed: ' + err.decode('utf-8'))
    out = out.decode('utf-8')

  dd = lxml.html.fromstring(out).find('dd')
  return ' '.join(str_inner(dd).split())


def make_bib_row(key, html):
  print(html, file=sys.stderr)
  return (key, html)


def insert_bib(dbh, key, html):
  bib_r = make_bib_row(key, html)
  dbh.execute(
    "INSERT INTO bib (key, data) VALUES (?, ?)",
    bib_r
  )


def process_bib(parser, trans, dbh, authors, filename):
  bib = parse_xml(parser, filename)
  key = str(bib.key)
  bibtex = str(trans(bib))
  html = make_bib_html(bibtex)
  insert_bib(dbh, key, html)


def main():
  parser = make_parser()
  trans = make_xslt(sys.argv[2])
  xml_to_db(parser, trans, process_bib, sys.argv[1], sys.argv[3])


if __name__ == '__main__':
  main()
