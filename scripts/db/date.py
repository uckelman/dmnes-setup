#!/usr/bin/python3 -b

import zeit

dates = (
  '1066',
  '1066-1068',
  'a 1066',
  'p 1066',
  '1066x1069',
  'f 1066',
  'f 1066x1067',
  '1066/7',
  'p c 1066',
  'a c 1066',
  '1066x1068',
  'c 1066',
  '1066?'
)

z = [(zeit.date_skey(d), d) for d in dates]
z.sort()

for i in z:
  print(i[0] >> 18, (i[0] >> 15) & 0x3, (i[0] >> 3) & 0xFFF, i[0] & 0x3, i[1])


