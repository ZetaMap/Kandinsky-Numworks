__all__ = ["Tests"]

def create_test(message, *valid_types):
  """
  Decorator to create the test. Put this before an empty method with (*objects, raise_err=True) arguments.

  The message must have {0} and {1} to format found type and required types.
  """
  if type(message) != str: raise TypeError("message must be an str")
  if len(valid_types) == 0: raise IndexError("one type or more must be specified")

  def decorator(self):
    type_msg = valid_types[0].__name__ if len(valid_types) == 1 else (", ".join([i.__name__ for i in valid_types[:-1]])+" or "+valid_types[-1].__name__)
    def wrapper(*objects, raise_err=True):
      for i in objects:
        if type(i) not in valid_types:
          if raise_err: raise TypeError(message.format(type(i).__name__, type_msg))
          else: return False

      return True
    return wrapper
  return decorator

class Tests:
  @create_test("can't convert {0} to {1}", int)
  def int(*objects, raise_err=True): ...

  @create_test("can't convert '{0}' object to {1} implicitly", str)
  def str(*objects, raise_err=True): ...

  @create_test("object '{0}' isn't a {1}", tuple, list)
  def list(*objects, raise_err=True): ...
