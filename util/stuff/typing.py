__all__ = [
  "register",
  "test"
]

_handle = {}

def register(type, msg):
  _handle[type] = msg

def test(_type, *fields):
  if _type not in _handle: raise ValueError("type '{_type}'")
  for i in fields:
    if type(i) != _type: raise TypeError(_handle[_type].format(type(i).__name__))
  return True