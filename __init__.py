"""A small module allowing to link the kandinsky module, from the Numworks, to a Windows window. 
Useful if you want to test your program without putting it on the calculator.
GitHub project: https://github.com/ZetaMap/Kandinsky-Numworks
"""

######### Imports #########

from os import getcwd
from pygame import QUIT, display as screen, image, draw, event, init
from pygame.font import Font
from math import floor


######### Program #########

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
  type_test(x, int)
  type_test(y, int)
  return Ks.get_pixel(x, y+Ks.TOP_SIZE)
  
def set_pixel(x, y, color):
  """Color pixel (x, y)"""
  type_test(x, int)
  type_test(y, int)
  type_test(color, [tuple, list])
  Ks.set_pixel(x, y+Ks.TOP_SIZE, convert_color(color))

def color(r, g, b):
  """Define a rgb color"""
  type_test(r, int)
  type_test(g, int)
  type_test(b, int)
  return convert_color((r, g, b))

def draw_string(text, x, y, color=(0,0,0), background=(255,255,255)):
  """Display a text from pixel (x, y)"""
  type_test(text, str)
  type_test(x, int)
  type_test(y, int)
  type_test(color, [tuple, list])
  type_test(background, [tuple, list])
  Ks.draw_string(text, x, y+Ks.TOP_SIZE-2, convert_color(color), convert_color(background))

def fill_rect(x, y, width, height, color):
  """Fill a rectangle at pixel (x, y)"""
  type_test(x, int)
  type_test(y, int)
  type_test(width, int)
  type_test(height, int)
  type_test(color, [tuple, list])
  Ks.fill_rect(x, y+Ks.TOP_SIZE, width, height, convert_color(color))
  
def display():
  run = True
  while run: 
    for i in event.get():
      if i.type == QUIT: run = False


######### Main class #########

class KS:
  TOP_SIZE = 19
  SCREEN = (320, 241)

  def __init__(self):
    init()
    path = getcwd()+'\\'
      
    self.root, self.windowFont, self.font = screen.set_mode(self.SCREEN), Font(path+"small_font.ttf", 12), Font(path+"large_font.ttf", 16)
    screen.set_caption("kandinsky - Numworks")
    screen.set_icon(image.load(path+"icon.ico"))
    
    self.root.fill((255, 255, 255))
    self.draw_content()
    screen.update()

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
    if y < self.TOP_SIZE: return (0, 0, 0)
    return convert_color(self.root.get_at((x, y))[:-1])

  def set_pixel(self, x, y, color):
    if y < self.TOP_SIZE: return

    draw.line(self.root, color, (x, y), (x, y))
    screen.flip()

  def draw_string(self, text, x, y, color, background):
    draw.rect(self.root, background, (x, y+2, len(text)*10, 18))
    self.root.blit(self.font.render(text, True, color), (x, y))
    if y < self.TOP_SIZE: self.draw_content()
    screen.flip()
  
  def fill_rect(self, x, y, width, height, color):
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
    
    draw.rect(self.root, color, (x, y, width, height))
    screen.flip()

Ks = KS()


######### Private method #########

def convert_color(color):
  if type(color) != list: color = list(color)
  if len(color) != 3: raise TypeError("Color needs 3 components")
  
  for i in range(len(color)):
    if color[i] > 255: color[i] %= 256
  return (floor(color[0] / 8) * 8, floor(color[1] / 4) * 4, floor(color[2] / 8) * 8)

"""Function taken from module: Python_Upgrade. 
link: https://github.com/ZetaMap/Python_Upgrade
"""
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


######### Example code #########

if __name__ == '__main__':
  """Source: https://my.numworks.com/python/andreanx/chromac
  """
  
  from cmath import *

  def hsv2color(h, s=1, v=1):
    h, c = (h/pi)%2, v*s
    x, m, k = c*(1-abs((h%(2/3))*3-1)), v-c, int(h*3)
    
    return color(
      round(255*(m+x*(k%3==1)+c*(k%5==0))), 
      round(255*(m+c*(k==1 or k==2)+x*(k%3==0))), 
      round(255*(m+x*(k%3==2)+c*(k==3 or k==4))))

  def modsv(p,m): return not(m) or (p*m)%1

  def chromac(xc=160, yc=110, rmax=110, ds=0, dv=0, tred=0, rev=False):
    xc, yc = round(xc), round(yc)
    
    for y in range(-rmax,rmax+1):
      xmin = round(sqrt(rmax**2-y**2).real)
      
      for x in range(-xmin,xmin+1):
        z = complex(x,y)
        r = abs(z)
        if r <= rmax: set_pixel(
          xc+x , yc+y,
          hsv2color((phase(z)-tred)*(1-2*rev), 
          modsv(r/rmax,ds),modsv(r/rmax,dv)))

  sw, sh, r = 320,220, 45
  lx3, ly2 = [r,(sw-1)/2,sw-1-r], [r,sh-1-r]
  lx2=[(lx3[0]+lx3[1])/2,(lx3[1]+lx3[2])/2]

  for x in range(2): chromac(lx2[x], sh/2, r, -1, not(x)*-1, x*pi/4, x%2)
  for y in range(2):
    for x in range(3): chromac(lx3[x], ly2[y], r, not(y), x-1, (2+3*y+x)*pi/4, (x+y)%2)
  
  display()
