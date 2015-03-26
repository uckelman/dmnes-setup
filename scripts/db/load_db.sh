#!/usr/bin/bash -ex

HERE=$(dirname $0)
DMNES=$1
DB=${2:-dmnes.sqlite}

rm -f $DB
sqlite3 $DB <$HERE/create.sql

$HERE/load_bib.py $DB $HERE/span.xsl $DMNES/bib

$HERE/load_cnf.py $DB $DMNES/schemata/cnf.xsd $HERE/span.xsl $DMNES/CNFs

$HERE/load_vnf.py $DB $DMNES/schemata/vnf.xsd $HERE/span.xsl $DMNES/VNFs
