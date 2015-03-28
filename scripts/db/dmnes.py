import lxml.etree
import lxml.objectify
import os
import os.path
import sqlite3
import subprocess
import sys


def make_db_handle(db):
  dbh = db.cursor()
  dbh.execute("PRAGMA foreign_keys = ON")
  return dbh


def x_for_y(dbh, table, xcol, ycol, yval):
  dbh.execute(
    "SELECT {} FROM {} WHERE {} = ?".format(xcol, table, ycol),
    (yval,)
  )
  row = dbh.fetchone()
  return row[0] if row else None


def str_inner(node):
  return ''.join(
    [node.text or ''] +
    [lxml.etree.tostring(c, encoding='unicode') for c in node.getchildren()] +
    [node.tail or '']
  )


def make_parser():
  return lxml.objectify.makeparser()


def make_validating_parser(filename):
  with open(filename) as f:
    doc = lxml.etree.parse(f)

  schema = lxml.etree.XMLSchema(doc)
  return lxml.objectify.makeparser(schema=schema, remove_blank_text=False)


def make_xslt(filename):
  with open(filename) as f:
    doc = lxml.etree.parse(f)
  return lxml.etree.XSLT(doc)


def parse_xml(parser, filename):
  with open(filename) as f:
    tree = lxml.objectify.parse(f, parser=parser)
  return tree.getroot()


def make_note_rows(ref, obj):
  return tuple((ref, str_inner(n)) for n in obj.note)


def insert_notes(dbh, table, ref, obj):
  if hasattr(obj, 'note'):
    note_rs = make_note_rows(ref, obj)
    dbh.executemany(
      "INSERT INTO {} (ref, note) VALUES (?,?)".format(table),
      note_rs
    )


def id_for_author(dbh, author):
  return x_for_y(dbh, 'authors', 'id', 'name', author)


def make_id_author_rows(id, author_ids):
  return tuple((id, aid) for aid in author_ids)


def insert_authors(dbh, table, id, filename):
  repo, filepath = os.path.split(filename)
  authors = log_to_authors(repo, filepath)
  author_ids = tuple(id_for_author(dbh, a) for a in authors)
  authors_rs = make_id_author_rows(id, author_ids)

  dbh.executemany(
    "INSERT INTO {} (ref, author) VALUES (?,?)".format(table),
    authors_rs
  )


AUTHORS = {
  'G. Grim'      : 'Genny Grim',
  'mariannsliz'  : 'Mariann Sliz',
  'Sara Uckelman': 'Sara L. Uckelman'
}


def log_to_authors(repo, path=None):
  cmd = "git log --format='%an'"
  if path:
    cmd += " --follow {}".format(path)

  print(cmd, file=sys.stderr)

  # get authors from git log
  with subprocess.Popen(cmd, cwd=repo, shell=True, stdout=subprocess.PIPE) as p:
    out = p.communicate(timeout=30)[0].decode('utf-8')

  authors = set(out.strip().split('\n'))

  # normalize author names
  return set(AUTHORS.get(a, a) for a in authors)


def xml_to_db(parser, trans, process, dbpath, xmlpath):
  # connect to the database
  with sqlite3.connect(dbpath) as db:
    dbh = make_db_handle(db)

    # process each XML file
    for root, _, files in os.walk(xmlpath):
      for f in files:
        if os.path.splitext(f)[1] == '.xml':
          fpath = os.path.join(root, f)
          try:
            process(parser, trans, dbh, fpath)
          except (lxml.etree.XMLSyntaxError, sqlite3.IntegrityError) as e:
            print(fpath, e, file=sys.stderr)
