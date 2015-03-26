#!/usr/bin/bash -ex

if [ "$#" -lt 1 ]; then
  echo "$0: Missing DMNES repo path." >&2
  exit 1
fi

if [ "$#" -gt 2 ]; then
  echo "$0: Too many arguments." >&2
  exit 1
fi

HERE=$(dirname $0)
DMNES=$1
DB=${2:-dmnes.sqlite}

rm -f $DB
sqlite3 $DB <$HERE/create.sql

$HERE/load_authors.py $DB $DMNES
$HERE/load_bib.py $DB $HERE/span.xsl $DMNES/bib
$HERE/load_cnf.py $DB $DMNES/schemata/cnf.xsd $HERE/span.xsl $DMNES/CNFs
$HERE/load_vnf.py $DB $DMNES/schemata/vnf.xsd $HERE/span.xsl $DMNES/VNFs
