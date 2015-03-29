#!/bin/bash -e

REPO=$1
SITE=$2

(echo -ne '\n\0' ; (cat $SITE/templates/*.html ; (find $REPO/bib $REPO/CNFs $REPO/VNFs -type f -print0 | xargs -0 -- xsltproc strip.xsl )) | tr -d '\n' | sed -e 's/./&\x00/g') | LC_COLLATE=C sort -zu | tr -d '\0'
