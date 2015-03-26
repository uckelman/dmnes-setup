#!/usr/bin/python3 -b

import sys

from dmnes import *


def make_shortname(name):
  s = name.split()
  return ' '.join([n[0] + '.' for n in s[:-1]] + s[-1:])


def make_author_rows(authors):
  return tuple((name, make_shortname(name)) for name in authors)


def process_authors(dbpath, repo):
  # connect to the database
  with sqlite3.connect(dbpath) as db:
    dbh = make_db_handle(db)

    authors = log_to_authors(repo)
    authors_rs = make_author_rows(authors)
    dbh.executemany(
      "INSERT INTO authors (name, shortname) VALUES (?,?)",
      authors_rs
    )


def main():
  process_authors(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
  main()
