"""A small module allowing to link the kandinsky module, from the Numworks, to a Windows window. 
Useful if you want to test your program without putting it on the calculator.
The [GitHub project](https://github.com/ZetaMap/Kandinsky-Numworks), and if you have any questions, check out the [FAQ](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md)
In addition, this module also emulates the drawing speed, and has [many other features](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/README.md#additional-features).
"""

from util.Core import Core as __Core

__all__ = [
  "get_pixel", 
  "set_pixel", 
  "color", 
  "draw_string", 
  "fill_rect",
  "quit"
]
__Core = __Core()


def get_pixel(x, y):
  """Return pixel (x, y) color"""
  pixel, err = __Core.event_fire(__Core.get_pixel, x, y)
  if err != None:
    raise err
  return pixel
  
def set_pixel(x, y, color):
  """Color pixel (x, y)"""
  _, err = __Core.event_fire(__Core.set_pixel, x, y, color)
  if err != None:
    raise err

def color(r, g=None, b=None):
  """Define a rgb color"""
  color, err = __Core.event_fire(__Core.color,r, g, b)
  if err != None:
    raise err
  return color

def draw_string(text, x, y, color=(0,0,0), background=(248,252,248)):
  """Display a text from pixel (x, y)"""
  _, err = __Core.event_fire(__Core.draw_string, text, x, y, color, background)
  if err != None:
    raise err

def fill_rect(x, y, width, height, color):
  """Fill a rectangle at pixel (x, y)"""
  _, err = __Core.event_fire(__Core.fill_rect, x, y, width, height, color)
  if err != None:
    raise err

def quit():
  """Close manualy the window without notifying the user"""
  __Core.stoped = True
