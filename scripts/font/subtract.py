#!/usr/bin/python3

import fontforge
import sys

chars = set(c for c in sys.stdin.read().strip())

for f in sys.argv[1:]:
    chars -= set(unichr(c.unicode) for c in fontforge.open(f).glyphs() if c.unicode != -1)

print(''.join(sorted(chars)), end='')
