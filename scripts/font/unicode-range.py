#!/usr/bin/python3

import itertools
import fontforge
import sys

f = fontforge.open(sys.argv[1])

# get list of code points
l = list(c.unicode for c in f.glyphs() if c.unicode != -1)
l.sort()

# convert list of code points into closed ranges
l = [(t[0][1], t[-1][1]) for t in (tuple(g[1]) for g in itertools.groupby(enumerate(l), lambda (i, x): i - x))]

# print the ranges
l = ['U+{:X}'.format(r[0]) if r[0] == r[1] else 'U+{:X}-{:X}'.format(r[0], r[1]) for r in l]

print(', '.join(l))
