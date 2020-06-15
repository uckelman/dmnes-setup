import lxml.etree
import lxml.objectify
import os
import os.path
import sqlite3
import subprocess
import sys


class RecordError(Exception):
  pass


def make_db_handle(db):
  dbh = db.cursor()
  dbh.execute("PRAGMA foreign_keys = ON")
  dbh.row_factory = sqlite3.Row
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


# normalize author names coming from git
AUTHORS_NORM = {
  'G. Grim'      : 'Genny Grim',
  'mariannsliz'  : 'Mariann Slíz',
  'Mariann Sliz' : 'Mariann Slíz',
  'Sara Uckelman': 'Sara L. Uckelman',
  'julpepe'      : 'Juliet Pepe'
}

AUTHORS_SKEY = {
  'Rebecca Le Get' : 'Le Get, Rebecca'
}

AUTHORS_SURNAME = {
  'Rebecca Le Get' : 'Le Get'
}

AUTHORS_PRENAMES = {
  'Rebecca Le Get' : 'Rebecca'
}

AUTHORS_PRENAMES_SHORT = {
  'Rebecca Le Get' : 'R.'
}


def id_for_author(dbh, author):
  return x_for_y(dbh, 'authors', 'id', 'name', author)


def make_id_author_rows(id, author_ids):
  return tuple((id, aid) for aid in author_ids)


def insert_authors(dbh, authors, table, id, filename):
  basename = os.path.splitext(os.path.basename(filename))[0]
  authors_rs = make_id_author_rows(id, authors[basename])

  dbh.executemany(
    "INSERT INTO {} (ref, author) VALUES (?,?)".format(table),
    authors_rs
  )


def authors_list(repo):
  cmd = "git log --format='%an'"
  # get authors from git log
  with subprocess.Popen(cmd, cwd=repo, shell=True, stdout=subprocess.PIPE) as p:
    out = p.communicate(timeout=30)[0].decode('utf-8')

  authors = set(out.strip().split('\n'))

  # normalize author names
  return set(AUTHORS_NORM.get(a, a) for a in authors)


# FIXME: timeout?
def log_to_authors(repo, basedir):
  authors = {}

  cmd = "git -c core.quotepath=false log --name-only --no-merges --format='%n %an' " + basedir
  with subprocess.Popen(cmd, cwd=repo, shell=True, stdout=subprocess.PIPE) as p:
    # skip blank first line
    next(p.stdout)
    for line in p.stdout:
      author = line.decode('utf-8').strip()
      # normalize author name
      author = AUTHORS_NORM.get(author, author)
      # skip blank line between author and filenames
      next(p.stdout)
      # get each modified filename
      for line in p.stdout:
        path = line.decode('utf-8').strip('"\n')
        if not path:
          break
        fkey, ext = os.path.splitext(os.path.basename(path))
        if ext == '.xml':
          authors.setdefault(fkey, set()).add(author)

  return authors


def author_id_map(dbh):
  return {
    '{} {}'.format(r[0], r[1]) : r[2]
    for r in dbh.execute('SELECT prenames, surname, id FROM authors')
  }


def file_author_id_map(authors, idmap):
  for k, v in authors.items():
    authors[k] = tuple(idmap[a] for a in v)
  return authors


def xml_to_db(parser, trans, process, dbpath, xmlpath):
  # build the authors map
  authors = log_to_authors(xmlpath, os.path.abspath(xmlpath))

  # connect to the database
  with sqlite3.connect(dbpath) as db:
    dbh = make_db_handle(db)

    # convert author names to ids in authors map
    idmap = author_id_map(dbh)
    authors = file_author_id_map(authors, idmap)

    # process each XML file
    for root, _, files in os.walk(xmlpath):
      for f in files:
        if os.path.splitext(f)[1] == '.xml':
          fpath = os.path.join(root, f)
          try:
            process(parser, trans, dbh, authors, fpath)
          except (
            lxml.etree.XMLSyntaxError, sqlite3.IntegrityError, RecordError
          ) as e:
            print(fpath, e, file=sys.stderr)

