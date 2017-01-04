#!/usr/bin/python3 -b

import unittest

import zeit


class ZeitTests(unittest.TestCase):

  def test_sort(self):
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

    parsed_dates = [(zeit.date_skey(d), d) for d in dates]
    parsed_dates.sort()

    exp = [
      'a 1066',
      'a c 1066',
      '1066',
      '1066/7',
      '1066?',
      'c 1066',
      'f 1066',
      '1066-1068',
      'f 1066x1067',
      '1066x1068',
      '1066x1069',
      'p 1066',
      'p c 1066',
    ]

    act = [d[1] for d in parsed_dates]    

    self.assertEqual(act, exp)


if __name__ == '__main__':
  unittest.main()
