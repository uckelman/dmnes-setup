#!/bin/bash -e

YEAR=$1
NUMBER=$2
DST=$3

wget -r -k -l0 -nH -P$DST/$YEAR/$NUMBER 'http://127.0.0.1:5000/names'
