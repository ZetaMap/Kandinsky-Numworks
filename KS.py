######### Imports #########

try: import pygame # Check if pygame is present
except ImportError: raise ImportError("""
>>> Pygame module is not installed on your system, and kandinsky depend to this module.
To install Pygame follow steps on the GitHub project: https://github.com/ZetaMap/Kandinsky-Numworks""")
else: del pygame

from pygame import QUIT, display as screen, image, draw, event, init
from pygame.font import Font
from math import floor


######### Main class #########

__all__ = []

class KS:
  TOP_SIZE = 19
  SCREEN = (320, 241)
  path = __file__[:__file__.rindex('\\')]+'\\'
  quit = False

  def __init__(self):
    init()
    self.quit = False
    self.root, self.windowFont, self.font = screen.set_mode(self.SCREEN), Font(self.path+"small_font.ttf", 12), Font(self.path+"large_font.ttf", 16)
    screen.set_caption("kandinsky - Numworks")
    screen.set_icon(image.load(self.path+"icon.ico"))
    
    self.root.fill((255, 255, 255))
    self.draw_content()
    self.refresh()

  def draw_content(self):
    draw.line(self.root, (0, 0, 0), (0, 0), (self.SCREEN[0], 0))
    draw.rect(self.root, "#ffb531", (0, 1, self.SCREEN[0], 18))
    self.root.blit(self.windowFont.render("deg", True, (255, 255, 255)), (5, 1))
    self.root.blit(self.windowFont.render("PYTHON", True, (255, 255, 255)), (139, 2))
    draw.line(self.root, (255, 255, 255), (300, 6), (300, 13))
    draw.rect(self.root, (255, 255, 255), (302, 6, 10, 8))
    draw.line(self.root, (255, 255, 255), (313, 6), (313, 13))
    draw.line(self.root, (255, 255, 255), (314, 8), (314, 11))

  def get_pixel(self, x, y):
    if self.quit: return
    type_test(x, int)
    type_test(y, int)

    if y < self.TOP_SIZE: return (0, 0, 0)
    return convert_color(self.root.get_at((x, y))[:-1])

  def set_pixel(self, x, y, color):
    if self.quit: return
    type_test(x, int)
    type_test(y, int)
    
    if y < self.TOP_SIZE: return
    draw.line(self.root, convert_color(color), (x, y), (x, y))
    self.refresh()

  def color(self, r, g, b):
    type_test(r, int)
    type_test(g, int)
    type_test(b, int)

    return convert_color((r, g, b))

  def draw_string(self, text, x, y, color, background):
    if self.quit: return
    type_test(text, str)
    type_test(x, int)
    type_test(y, int)

    draw.rect(self.root, convert_color(background), (x, y+2, len(text)*10, 18))
    self.root.blit(self.font.render(text, True, convert_color(color)), (x, y))
    if y < self.TOP_SIZE: self.draw_content()
    self.refresh()
  
  def fill_rect(self, x, y, width, height, color):
    if self.quit: return
    type_test(x, int)
    type_test(y, int)
    type_test(width, int)
    type_test(height, int)
      
    if width < 0: 
      x += width
      width *= -1
    if height < 0:
      y += height
      height *= -1
    if y < self.TOP_SIZE and y+height > self.TOP_SIZE: 
      height -= self.TOP_SIZE-y
      y = self.TOP_SIZE
    elif y+height <= self.TOP_SIZE: return
    
    draw.rect(self.root, convert_color(color), (x, y, width, height))
    self.refresh()

  def display(self):
    while not self.quit: self.refresh(False)
    
  def refresh(self, withError=True):
    try: screen.flip()
    except: self.quit = True
    else: 
      for i in event.get():
        if i.type == QUIT: 
          screen.quit()
          self.quit = True
          if withError: raise RuntimeError("kandinsky window destroyed")

Ks = KS()


def convert_color(color):
  type_test(color, [tuple, list, str])

  if type(color) == str: return color
  elif type(color) != list: color = list(color)
  if len(color) != 3: raise TypeError("Color needs 3 components")
  
  for i in range(len(color)):
    if color[i] > 255: color[i] %= 256
  return (floor(color[0] / 8) * 8, floor(color[1] / 4) * 4, floor(color[2] / 8) * 8)

"""Function taken from module [Python_Upgrade](https://github.com/ZetaMap/Python_Upgrade)"""
def type_test(_object, _type, canBeNone=False, withError=True, contentException=None):
  """Allows you to test an object ('_object') with a type or a type list ('_type'), 
  and tell it if we want it to return an error or the correct type ('withError'), by default 'withError' = True.

  \nIt is also possible to tell it if the object can be None ('canBeNone') 
  and/or if you want to ignore a content ('contentException').
  """
  ### v Testing fonction v ###  
  if not callable(_type) and type(_type) == list:
    if len(_type) == 0: raise IndexError("the type list must have at least one occurrence")
    for i in _type: 
      if not callable(i): raise TypeError("the list must only contain types")
  else: _type = [_type]
  ### ^ Testing fonction ^ ###

  if canBeNone:
    for i in _type:
      if _object == None or type(_object) == i: 
        correct = i
        break
      elif _object == contentException: 
        correct = True
        break
      else: correct = False
  else:
    for i in _type:
      if type(_object) == i: 
        correct = i
        break
      elif contentException != None and _object == contentException:
        correct = True
        break
      else: correct = False

  if withError: 
    if correct != False: return correct
    else:
      typeList = ""
      for i in range(len(_type)): typeList += "'"+_type[i].__name__+("', " if i != len(_type)-2 else "' or ")
      error = "'{}' is not valid as type argument {}".format(type(_object).__name__, typeList.rstrip(" ,"))
      raise TypeError(error)
  else:
    if correct: return True
    else: return False
