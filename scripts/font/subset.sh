#!/bin/bash -e

REPO=$1
SITE=$2
OUT=$(realpath $3)
shift 3

./chars.sh $REPO $SITE >chars

while [ $# -gt 0 ]; do
  IN=$(realpath $1)
  OFILE=$(basename -s .ttf $IN)Subset.ttf
  pushd font-optimizer
  ./subset.pl --charsfile=../chars $IN $OUT/$OFILE
  popd
  sfnt2woff $OUT/$OFILE
  mkeot $OUT/$OFILE >$OUT/$(basename -s .ttf $OFILE).eot
  shift
done

