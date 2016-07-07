#!/bin/bash -e

repo=$1
site=$2

(cat $site/templates/*.html ; find $repo/bib $repo/CNFs $repo/VNFs -type f -print0 | xargs -0 -- xsltproc strip.xsl ) | tr -d '\n\r' | sed 's/./&\x00/g' | LC_COLLATE=C sort -uz | tr -d '\0'
