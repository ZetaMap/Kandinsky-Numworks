######### Imports #########

try: import pygame # Check if pygame is present
except ImportError: raise ImportError("""
>>> Pygame module is not installed on your system, and kandinsky depend to this module.
To install Pygame follow steps on the GitHub project: https://github.com/ZetaMap/Kandinsky-Numworks""")
else: del pygame

from pygame import display as screen, image, draw, event, key, init
from pygame.constants import KEYDOWN, QUIT, KMOD_CTRL, K_m
from pygame.font import Font
from pygame.time import wait
from math import floor


######### Main class #########

__all__ = []

class KS:
  init()
  APP_NAME = "kandinsky"
  TOP_SIZE = 34
  SCREEN = (320, 256)
  PATH = __file__[:__file__.rindex('\\')]+'\\'
  quit = False
  mode = 0
  modes = ("Numworks mode", "Omega mode", 'Machine power')

  def __init__(self):
    self.root = screen.set_mode(self.SCREEN)
    self.windowFont, self.font = Font(self.PATH+"small_font.ttf", 12), Font(self.PATH+"large_font.ttf", 16)
    
    screen.set_caption(self.APP_NAME)
    screen.set_icon(image.load(self.PATH+"icon.ico"))

    self.root.fill("white")
    self.draw_content()
    self.refresh()

  def draw_content(self):
    draw.rect(self.root, "white", (0, 0, 320, 15))
    self.root.blit(self.windowFont.render("M+CTRL: to change the refresh mode", True, "black"), (2, 0))
    draw.line(self.root, "black", (0, 15), (self.SCREEN[0], 15))
    draw.rect(self.root, "#ffb531" if self.mode == 0 or self.mode == 2 else "#c53431", (0, 16, self.SCREEN[0], 18))
    self.root.blit(self.windowFont.render("deg" if self.mode == 0 or self.mode == 2 else "sym/deg", True, "white"), (5, 16))
    self.root.blit(self.windowFont.render("PYTHON", True, "white"), (139, 17))
    if self.mode == 0 or self.mode == 2:
      draw.line(self.root, "white", (300, 21), (300, 28))
      draw.rect(self.root, "white", (302, 21, 10, 8))
      draw.line(self.root, "white", (313, 21), (313, 28))
      draw.line(self.root, "white", (314, 23), (314, 26))
    else:
      draw.line(self.root, "white", (260, 21), (260, 28))
      draw.rect(self.root, "white", (262, 21, 10, 8))
      draw.line(self.root, "white", (273, 21), (273, 28))
      draw.line(self.root, "white", (274, 23), (274, 26))
      self.root.blit(self.windowFont.render("12:00", True, "white"), (280, 17))

  def get_pixel(self, x, y):
    if self.quit: return
    type_test(x, int)
    type_test(y, int)

    if y < self.TOP_SIZE: return (0, 0, 0)
    return self.convert_color(self.root.get_at((x, y))[:-1])

  def set_pixel(self, x, y, color):
    if self.quit: return
    type_test(x, int)
    type_test(y, int)
    
    if y < self.TOP_SIZE: return
    draw.line(self.root, self.convert_color(color), (x, y), (x, y))
    self.refresh()

  def color(self, r, g, b):
    type_test(r, int)
    type_test(g, int)
    type_test(b, int)

    return self.convert_color((r, g, b))

  def draw_string(self, text, x, y, color, background):
    if self.quit: return
    type_test(text, str)
    type_test(x, int)
    type_test(y, int)

    draw.rect(self.root, self.convert_color(background), (x, y+2, len(text)*10, 18))
    self.root.blit(self.font.render(text, True, self.convert_color(color)), (x, y))
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
    
    draw.rect(self.root, self.convert_color(color), (x, y, width, height))
    self.refresh()

  def display(self):
    while not self.quit: self.refresh(False)
    
  def refresh(self, withError=True):
    try: screen.flip()
    except: self.quit = True
    else: 
      if self.mode == 0: wait(2)
      elif self.mode == 1: wait(1)

      for e in event.get():
        if e.type == QUIT: 
          screen.quit()
          self.quit = True
          if withError: raise RuntimeError("kandinsky window destroyed")
        
        elif e.type == KEYDOWN: 
          if key.get_mods() & KMOD_CTRL and key.get_pressed()[K_m]:
            self.mode += 1
            if self.mode == 3: self.mode = 0
            screen.set_caption(self.APP_NAME+": "+self.modes[self.mode])
            self.draw_content()

  def convert_color(self, color):
    type_test(color, [tuple, list, str])

    if type(color) == str: 
      self.root.set_at((0, 0), color)
      color = self.root.get_at((0, 0))[:-1]
      self.root.set_at((0, 0), "white")
    elif type(color) == tuple: color = list(color)
    if len(color) != 3: raise TypeError("Color needs 3 components")
    
    for i in range(len(color)):
      if color[i] > 255: color[i] %= 256
    return (floor(color[0] / 8) * 8, floor(color[1] / 4) * 4, floor(color[2] / 8) * 8)

Ks = KS()


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
