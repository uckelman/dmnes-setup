#!/bin/bash -e

YEAR=$1
NUMBER=$2
DST=$3

wget -r -k -l0 -nH --restrict-file-names=nocontrol -P$DST/$YEAR/$NUMBER 'https://127.0.0.1:5000/names'

# fix exentsions of .eot fonts
for i in $(find $DST/$YEAR/$NUMBER -name *.eot?) ; do mv $i $(echo $i | sed 's/?$//') ; done
