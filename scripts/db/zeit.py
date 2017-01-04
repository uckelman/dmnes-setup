import ctypes
import os.path


class Date(ctypes.Structure):
  _fields_ = [
    ('year', ctypes.c_short * 2),
    ('anp', ctypes.c_byte),
    ('flags', ctypes.c_ubyte)
  ]

  def __str__(self):
    return str((self.year[0], self.year[1], self.anp, self.flags))


class Zeit(ctypes.Structure):
  _fields_ = [
    ('floruit', ctypes.c_bool),
    ('beg', Date),
    ('end', Date)
  ]

  def __str__(self):
    if self.end.year[0]:
      return '{} [{}, {}]'.format(self.floruit, self.beg, self.end)
    else:
      return '{} {}'.format(self.floruit, self.beg)

  def __lt__(self, other):
    return compare_zeit(ctypes.byref(self), ctypes.byref(other)) == -1
    
  def __le__(self, other):
    return self < other or self == other

  def __eq__(self, other):
    return compare_zeit(ctypes.byref(self), ctypes.byref(other)) == 0

  def __ne__(self, other):
    return not self == other
  
  def __gt__(self, other):
    return compare_zeit(ctypes.byref(self), ctypes.byref(other)) == 1

  def __ge__(self, other):
    return self > other or self == other


LIBPATH = os.path.join(os.path.dirname(__file__), 'libdate.so')
lib = ctypes.cdll.LoadLibrary(LIBPATH)

create = lib.create_zeit
create.argtypes = [ ctypes.c_char_p ]
create.restype = Zeit

compare = lib.compare_zeit
compare.argtypes = [ ctypes.POINTER(Zeit), ctypes.POINTER(Zeit) ]
compare.restype = ctypes.c_int

key = lib.key_zeit
key.argtypes = [ ctypes.POINTER(Zeit) ]
key.restype = ctypes.c_uint64


def date_skey(d):
  return key(ctypes.byref(create(d.encode('utf-8'))))
