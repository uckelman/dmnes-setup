#!/usr/bin/bash -ex

DMNES=$1

rm -f dmnes.sqlite
sqlite3 dmnes.sqlite <create.sql

find $DMNES/bib -type f -print0 | xargs -0 ./load_bib.py dmnes.sqlite span.xsl

find $DMNES/CNFs -type f -print0 | xargs -0 ./load_cnf.py dmnes.sqlite $DMNES/schemata/cnf.xsd span.xsl

find $DMNES/VNFs -type f -print0 | xargs -0 ./load_vnf.py dmnes.sqlite $DMNES/schemata/vnf.xsd span.xsl
