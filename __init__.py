"""A small module allowing to link the kandinsky module, from the Numworks, to a Windows window. 
Useful if you want to test your program without putting it on the calculator.
The [GitHub project](https://github.com/ZetaMap/Kandinsky-Numworks), and if you have any questions, check out the [FAQ](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md)
"""
from .util.Core import Core as __Core

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
  try: return __Core.get_pixel(x, y)
  except Exception as e:
    raise \
      e if __Core.DEBUG else e.with_traceback(None)
  
def set_pixel(x, y, color):
  """Color pixel (x, y)"""
  try: __Core.set_pixel(x, y, color)
  except Exception as e: 
    raise \
      e if __Core.DEBUG else e.with_traceback(None)

def color(r, g=None, b=None):
  """Define a rgb color"""
  try: return __Core.color(r, g, b)
  except Exception as e: 
    raise \
      e if __Core.DEBUG else e.with_traceback(None)

def draw_string(text, x, y, color=(0,0,0), background=(248,252,248)):
  """Display a text from pixel (x, y)"""
  try: __Core.draw_string(text, x, y, color, background)
  except Exception as e: 
    raise \
      e if __Core.DEBUG else e.with_traceback(None)

def fill_rect(x, y, width, height, color):
  """Fill a rectangle at pixel (x, y)"""
  try: __Core.fill_rect(x, y, width, height, color)
  except Exception as e: 
    raise \
      e if __Core.DEBUG else e.with_traceback(None)
  
def display(justRefresh=False):
  """Run an infinite loop (a little modified) allowing to keep the window open
  If justRefresh == True: Just refresh the screen and don't run the loop.
  """
  try: 
    if justRefresh: __Core.refresh()
    else: __Core.display()
  except Exception as e:
    raise \
      e if __Core.DEBUG else e.with_traceback(None)
