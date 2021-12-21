try: from kandinsky.util.demo import *
except ImportError as e: 
  if e.msg.lower() == "no module named 'ion'": print("""
>>> Ion module is not installed on your system.
To install it, type 'pip install ion-Numworks' in a command prompt.""")
  else: print("Error: demo.py can't be load!")
