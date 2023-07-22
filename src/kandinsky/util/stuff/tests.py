__all__ = ["Tests"]

def create_test(message, *valid_types):
  """
  Decorator to create the test. Put this before an empty method with (*objects, raise_err=True) arguments.

  The message can contains {found} and {valid} keys to format found type and required types.
  """
  if type(message) != str: raise TypeError("message must be an str")
  if len(valid_types) == 0: raise IndexError("one type or more must be specified")
  if not all(issubclass(type(t), type) for t in valid_types): raise TypeError("valid_types must be a list of types")

  def decorator(func):
    type_msg = valid_types[0].__name__ if len(valid_types) == 1 else (", ".join([i.__name__ for i in valid_types[:-1]])+" or "+valid_types[-1].__name__)
    def wrapper(*objects, raise_err=True):
      for i in objects:
        if type(i) not in valid_types:
          if raise_err: raise TypeError(message.format(found=type(i).__name__, valid=type_msg))
          else: return False

      return True
    return wrapper
  return decorator

class Tests:
  @create_test("can't convert {found} to {valid}", int)
  def int(*objects, raise_err=True): ...

  @create_test("can't convert {found!r} object to {valid} implicitly", str)
  def str(*objects, raise_err=True): ...

  @create_test("object {found!r} isn't a {valid}", tuple, list)
  def list(*objects, raise_err=True): ...
