"""A small module allowing to link the kandinsky module, from the Numworks, to a Windows window. 
Useful if you want to test your program without putting it on the calculator.
The [GitHub project](https://github.com/ZetaMap/Kandinsky-Numworks), and if you have any questions, check out the [FAQ](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md)
"""
try: from .KS import Ks
except: from KS import Ks

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
  return Ks.get_pixel(x, y+Ks.TOP_SIZE)
  
def set_pixel(x, y, color):
  """Color pixel (x, y)"""
  Ks.set_pixel(x, y+Ks.TOP_SIZE, color)

def color(r, g, b):
  """Define a rgb color"""
  return Ks.color(r, g, b)

def draw_string(text, x, y, color=(0,0,0), background=(248,252,248)):
  """Display a text from pixel (x, y)"""
  Ks.draw_string(text, x, y+Ks.TOP_SIZE-2, color, background)

def fill_rect(x, y, width, height, color):
  """Fill a rectangle at pixel (x, y)"""
  Ks.fill_rect(x, y+Ks.TOP_SIZE, width, height, color)
  
def display():
  """Run an infinite loop (a little modified) allowing to keep the window open"""
  Ks.display()


######### Example code #########

if __name__ == '__main__':
  try: from .demo import *
  except ImportError: from demo import *