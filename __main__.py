try: from .util.demo import *
except ImportError: 
  try: from util.demo import *
  except ImportError: print("Error: demo.py can't be load!")
  except Exception as e:
    raise \
      e.with_traceback(None)