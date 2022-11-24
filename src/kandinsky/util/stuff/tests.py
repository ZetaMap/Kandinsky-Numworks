__all__ = ["Tests"]

def _test_wrapper(message, *types):
  if len(types) == 0: raise IndexError("one type or more must be specified")

  def decorator(_):
    type_msg = types[0].__name__ if len(types) == 1 else (", ".join([i.__name__ for i in types[:-1]])+" or "+types[-1].__name__)
    def wrapper(*objects, raise_err=True):
      for i in objects:
        if type(i) not in types: 
          if raise_err: raise TypeError(message.format(type(i).__name__, type_msg))
          else: return False
          
      return True
    return wrapper
  return decorator

class Tests:
  @_test_wrapper("can't convert {0} to {1}", int)
  def int_test(*objects, raise_err=True): ...

  @_test_wrapper("can't convert '{0}' object to {1} implicitly", str)
  def str_test(*objects, raise_err=True): ...

  @_test_wrapper("object '{0}' isn't a {1}", tuple, list)
  def list_test(*objects, raise_err=True): ...
