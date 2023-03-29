try: from .util.demo import *
except ImportError as e: 
  if e.msg.lower() == "no module named 'ion'": e.msg = ("ion module isn't installed, type 'pip install ion-numworks' to install it.",)
  print(f"Error: demo can't be load! ({e.msg})")
