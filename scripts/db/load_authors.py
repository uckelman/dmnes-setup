#!/usr/bin/python3 -b

import sys

from dmnes import *


def make_author_rows(authors):
  return tuple(
    (
      AUTHORS_SURNAME.get(a, a.rsplit(maxsplit=1)[-1]),
      AUTHORS_SKEY.get(a, ', '.join(reversed(a.rsplit(maxsplit=1)))),
      AUTHORS_PRENAMES.get(a, a.rsplit(maxsplit=1)[0]),
      AUTHORS_PRENAMES_SHORT.get(a, ''.join(n[0]+'.' for n in a.rsplit()[:-1]))
    ) for a in authors
  )


def process_authors(dbpath, repo):
  # connect to the database
  with sqlite3.connect(dbpath) as db:
    dbh = make_db_handle(db)

    authors = authors_list(repo)
    authors_rs = make_author_rows(authors)
    dbh.executemany(
      "INSERT INTO authors (surname, skey, prenames, prenames_short) VALUES (?,?,?,?)",
      authors_rs
    )


def main():
  process_authors(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
  main()
