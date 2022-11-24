"""A small module allowing to link the kandinsky module, from the Numworks, to a Windows window. 
Useful if you want to test your program without putting it on the calculator.
The [GitHub project](https://github.com/ZetaMap/Kandinsky-Numworks), and if you have any questions, check out the [FAQ](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md)
In addition, this module also emulates the drawing speed, and has [many other features](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/README.md#additional-features).
"""

try: from .util.core import DEFAULT_OS, Core as __Core
except ImportError: from util.core import DEFAULT_OS, Core as __Core

__name__ = "kandinsky"
__version__ = "null"
try: __doc__ = open("README.md").read()
except FileNotFoundError: __doc__ = "<unknown>"
__all__ = [ 
  #numworks 
  "get_pixel", 
  "set_pixel", 
  "color", 
  "draw_string",
  "fill_rect",

  #new only for Computer
  "quit",

  #omega
  "draw_line",
  "wait_vblank",
  "get_keys",

  #upsilon
  "draw_circle",
  "fill_circle",
  "fill_polygon",
  "get_palette"
]
__Core = __Core()
try: OS_MODE = __Core.OS_MODE
except AttributeError: OS_MODE = DEFAULT_OS


# Numworks basic methods
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

# Argument added by Upsilon
if OS_MODE == 3:
  def draw_string(text, x, y, color=(0,0,0), background=(248,252,248), font=False):
    """Display a text from pixel (x, y)"""
    _, err = __Core.event_fire(__Core.draw_string, text, x, y, color, background, font)
    if err != None:
      raise err  
else :
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

# new method of kandinsky, only on Computer
def quit():
  """Close manualy the window without notifying the user"""
  _, err = __Core.event_fire(__Core.quit_app)
  if err != None:
    raise err

# omega methods
def draw_line(x1, y1, x2, y2, color):
  """Draw a line at (x1, y1) to (x2, y2)"""
  _, err = __Core.event_fire(__Core.draw_line, x1, y1, x2, y2, color)
  if err != None:
    raise err

def wait_vblank():
  """Wait for screen refresh"""
  _, err = __Core.event_fire(__Core.wait_vblank)
  if err != None:
    raise err

def get_keys():
  """Get pressed keys"""
  keys, err = __Core.event_fire(__Core.get_keys)
  if err != None:
    raise err
  return keys

# upsilon methods
def draw_circle(x, y, r, color):
  """Draw circle at (x, y) of radius r"""
  _, err = __Core.event_fire(__Core.draw_circle, x, y, r, color)
  if err != None:
    raise err

def fill_circle(x, y, r, color):
  """Fill circle at (x, y) of radius r"""
  _, err = __Core.event_fire(__Core.fill_circle, x, y, r, color)
  if err != None:
    raise err

def fill_polygon(points, color):
  """Fill polygon at points [(x1, y1), ...]"""
  _, err = __Core.event_fire(__Core.fill_polygon, points, color)
  if err != None:
    raise err

def get_palette():
  """Get upsilon theme palette"""
  pal, err = __Core.event_fire(__Core.get_palette)
  if err != None:
    raise err
  return pal


######### Clean #########
# delete methods according to OS
if OS_MODE: 
  # upsilon moved this method and epsilon don't have this
  if OS_MODE == 3 or OS_MODE == 1:
    __all__.remove("get_keys")
    del get_keys

  # delete upsilon methods
  if OS_MODE < 3: 
    __all__.remove("draw_circle")
    __all__.remove("fill_circle")
    __all__.remove("fill_polygon")
    __all__.remove("get_palette")
    del draw_circle, fill_circle,  fill_polygon, get_palette
 
  # delete omega methods
  if OS_MODE < 2: 
    __all__.remove("draw_line")
    __all__.remove("wait_vblank")
    del draw_line, wait_vblank
        
# Cleanup namespaces
del OS_MODE, DEFAULT_OS