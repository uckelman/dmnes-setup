#!/usr/bin/python3 -b

import re
import sys

from dmnes import *


def paragraphize(s):
  return '\n'.join('<p>{}</p>'.format(p.strip()) for p in re.split('\n{2,}', s))


def make_cnf_row(cnf):
  return (
    str(cnf.nym),
    str(cnf.gen),
    str_inner(cnf.etym),
    paragraphize(str_inner(cnf.usg)) if hasattr(cnf, 'usg') else None,
    paragraphize(str_inner(cnf['def'])) if hasattr(cnf, 'def') else None,
    1 if cnf.meta.live else 0
  )


def insert_cnf(dbh, cnf):
  cnf_r = make_cnf_row(cnf)
  dbh.execute(
    "INSERT INTO cnf (nym, gen, etym, usg, def, live) VALUES (?,?,?,?,?,?)",
    cnf_r
  )
  return dbh.lastrowid


def process_cnf(parser, trans, dbh, authors, filename):
  cnf = parse_xml(parser, filename)
  spanned_cnf = trans(cnf).getroot()
  cnf_id = insert_cnf(dbh, spanned_cnf)
  insert_notes(dbh, "cnf_notes", cnf_id, spanned_cnf)
  insert_authors(dbh, authors, "cnf_authors", cnf_id, filename)


def main():
  parser = make_validating_parser(sys.argv[2])
  trans = make_xslt(sys.argv[3])
  xml_to_db(parser, trans, process_cnf, sys.argv[1], sys.argv[4])


if __name__ == '__main__':
  main()
