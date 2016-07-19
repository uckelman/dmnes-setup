#!/bin/bash -ex

for otf in "$@"; do
  base=$(basename -s .otf "$otf")
  sfnt2woff "$otf"
  python -c "import fontforge
fontforge.open('$otf').generate('${base}.ttf')"
  mkeot "${base}.ttf" >"${base}.eot"
  woff2/woff2_compress "${base}.ttf"
done
