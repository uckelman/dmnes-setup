#!/usr/bin/bash -ex

HERE=$(dirname $0)
DMNES=$1
DB=${2:-dmnes.sqlite}

sqlite3 $DB <$HERE/create.sql

find $DMNES/bib -type f -name *.xml -print0 | xargs -0 $HERE/load_bib.py $DB $HERE/span.xsl

find $DMNES/CNFs -type f -name *.xml -print0 | xargs -0 $HERE/load_cnf.py $DB $DMNES/schemata/cnf.xsd $HERE/span.xsl

find $DMNES/VNFs -type f -name *.xml -print0 | xargs -0 $HERE/load_vnf.py $DB $DMNES/schemata/vnf.xsd $HERE/span.xsl
