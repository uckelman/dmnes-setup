#!/bin/bash -ex

repo=$1
site=$2
remaining_ok=$3
shift 3

if [[ ! -f chars0 ]]; then
  ./chars.sh $repo $site >chars0
fi
cp chars0 chars

for font in "$@"; do
  base=$(basename -s .otf "$font")
  pyftsubset "$font" --text-file=chars --output-file="${base}Subset.otf"
  mv chars chars~
  ./subtract.py "${base}Subset.otf" <chars~ >chars
done

remaining=$(cat chars)
echo "Characters remaining: $remaining"
if [[ -n "$remaining" && $remaining_ok -eq 0 ]]; then
  exit 1
fi
