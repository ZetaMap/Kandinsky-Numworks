try: from .util.demo import *
except ImportError: 
  try: from util.demo import *
  except: print("Error: demo.py can't be load!")