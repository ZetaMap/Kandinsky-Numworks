"""A small module allowing to link the kandinsky module, from the Numworks, to a Windows window. 
Useful if you want to test your program without putting it on the calculator.
The [GitHub project](https://github.com/ZetaMap/Kandinsky-Numworks), and if you have any questions, check out the [FAQ](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md)
"""
try: from .util.KS import Ks as __Ks
except: 
  try: from util.KS import Ks as __Ks
  except: pass

__all__ = [
  "get_pixel", 
  "set_pixel", 
  "color", 
  "draw_string", 
  "fill_rect",
  "display"
]

def get_pixel(x, y):
  """Return pixel (x, y) color"""
  return __Ks.get_pixel(x, y)
  
def set_pixel(x, y, color):
  """Color pixel (x, y)"""
  try: __Ks.set_pixel(x, y, color)
  except Exception as e: 
    raise \
      e.with_traceback(None)

def color(r, g, b):
  """Define a rgb color"""
  try: return __Ks.color(r, g, b)
  except Exception as e: 
    raise \
      e.with_traceback(None)

def draw_string(text, x, y, color=(0,0,0), background=(248,252,248)):
  """Display a text from pixel (x, y)"""
  try: __Ks.draw_string(text, x, y-2, color, background)
  except Exception as e: 
    raise \
      e.with_traceback(None)

def fill_rect(x, y, width, height, color):
  """Fill a rectangle at pixel (x, y)"""
  try: __Ks.fill_rect(x, y, width, height, color)
  except Exception as e: 
    raise \
      e.with_traceback(None)
  
def display():
  """Run an infinite loop (a little modified) allowing to keep the window open"""
  __Ks.display()


######### Example code #########

if __name__ == '__main__':
  try: from .util.demo import *
  except ImportError: 
    try: from util.demo import *
    except: pass