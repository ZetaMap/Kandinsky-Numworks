"""A small module allowing to link the kandinsky module, from the Numworks, to a Windows window. 
Useful if you want to test your program without putting it on the calculator.
GitHub project: https://github.com/ZetaMap/Kandinsky-Numworks
"""

######### Imports #########

from sys import path
from tkinter import Tk, Canvas, font
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

  if Ks.FIRST_PIXEL: return (0, 0, 0)
  Ks.get_pixel(x+3, y+20)
  
def set_pixel(x, y, color):
  """Color pixel (x, y)"""
  type_test(x, int)
  type_test(y, int)
  type_test(color, tuple)

  #if Ks.FIRST_PIXEL: Ks.window()
  Ks.set_pixel(x+3, y+21, color)

def color(r, g, b):
  """Define a rgb color"""
  type_test(r, int)
  type_test(g, int)
  type_test(b, int)
  
  return Ks.convert_color((r, g, b), False)

def draw_string(text, x, y, color=(0,0,0), background=(255,255,255)):
  """Display a text from pixel (x, y)"""
  type_test(text, str)
  type_test(x, int)
  type_test(y, int)
  type_test(color, tuple)
  type_test(background, tuple)
  
  #if Ks.FIRST_PIXEL: Ks.window()    
  Ks.draw_string(text, x+3, y+20, color, background)

def fill_rect(x, y, width, height, color):
  """Fill a rectangle at pixel (x, y)"""
  type_test(x, int)
  type_test(y, int)
  type_test(width, int)
  type_test(height, int)
  type_test(color, tuple)
  
  #if Ks.FIRST_PIXEL: Ks.window()
  Ks.fill_rect(x+3, y+21, width, height, color)
  
def display_(func=None):
  if func != None: Ks.canvas.after(1, func)
  Ks.root.mainloop()


######### Main class #########

class KS:
  FIRST_PIXEL = True
  first_ground = []

  def __init__(self):
    """Create the window if the fisrt pixel is colored"""
 
    def default(): 
      self.FIRST_PIXEL = True
      self.root.quit()
    
    self.root, self.windowFont, self.font = Tk(), font.Font(family="Consolas", size=10), font.Font(family="Source Pixel Large", size=12)
    self.canvas = Canvas(self.root, bg="white", width=323, height=242)
    self.root.title("kandinsky - Numworks")
    self.root.iconbitmap(path+"icon.ico")
    self.root.geometry("326x246+640+360")
    self.root.resizable(False, False)

    self.first_ground.append(self.canvas.create_rectangle(2, 2, 323, 243))
    self.first_ground.append(self.canvas.create_rectangle(3, 3, 322, 20, fill="#ffb531", outline="#ffb531"))
    self.first_ground.append(self.canvas.create_text(8, 3, text="deg", fill="white", font=self.windowFont, anchor="nw"))
    self.first_ground.append(self.canvas.create_text(160, 11, text="PYTHON", fill="white", font=self.windowFont))
    self.first_ground.append(self.canvas.create_line(302, 7, 302, 15, fill="white"))
    self.first_ground.append(self.canvas.create_rectangle(304, 7, 313, 14, fill="white", outline="white"))
    self.first_ground.append(self.canvas.create_line(315, 7, 315, 15, fill="white"))
    self.first_ground.append(self.canvas.create_line(316, 9, 316, 13, fill="white"))
    self.canvas.pack()
    self.canvas.update()

    self.root.protocol("WM_DELETE_WINDOW", default)
    self.FIRST_PIXEL = False

#  def window(self):
#    pass

  def get_pixel(self, x, y):
    if x < 3 or y < 20 or x > 322 or y > 242: return (0, 0, 0)
    return self.canvas.find_closest(x, y)

  def set_pixel(self, x, y, color):
    if x < 3 or y < 20 or x > 322 or y > 242: return
    self.canvas.create_line(x, y, x+1, y+1, fill=self.convert_color(color))
    self.canvas.update()

  def draw_string(self, text, x, y, color, background):
    self.canvas.create_rectangle(x, y+1, x+len(text)*10, y+19, fill=self.convert_color(background), width=0)
    self.canvas.create_text(x, y, text=text, fill=self.convert_color(color), font=self.font, anchor="nw")
    for i in self.first_ground: self.canvas.tag_raise(i)
    self.canvas.update()
    

  def fill_rect(self, x, y, width, height, color):
    if x < 3 or y < 20 or x > 322 or y > 242: return
    if width == 0 or height == 0: return
    if (x+width > 322 or x+width < 3) and width != 1: width = 323-x if x+width > 322 else 3-x
    if (y+height > 242 or y+height < 21) and height != 1: height = 243-y if y+height > 242 else 21-y

    self.canvas.create_rectangle(x, y, x+width, y+height, fill=self.convert_color(color), width=0)
    self.canvas.update()

  def convert_color(self, color, returnHex=True):
    color = list(color)
    if len(color) != 3: raise TypeError("Color needs 3 components")
    
    for i in range(len(color)):
      if color[i] > 255: color[i] %= 256
    if returnHex: return "#{0:02x}{1:02x}{2:02x}".format(
        floor(color[0] / 8) * 8, 
        floor(color[1] / 4) * 4,
        floor(color[2] / 8) * 8)
    else: return (
        floor(color[0] / 8) * 8, 
        floor(color[1] / 4) * 4,
        floor(color[2] / 8) * 8)


######### Private method #########

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


######### Module init #########

for i in path:
  if i.endswith("site-packages"):
    path = i+"\\kandinsky\\"
    break
Ks = KS()
if not "Source Pixel Large" in font.families(Ks.root): print(
"""RuntimeWarning: The font used by the module ('Source Pixel Large') is not installed on your system!
/!\\ If you don't install it, the texts display will not be correct. /!\\
To install it:
  1- open the indicated file: {}
  2- click on the button 'Install', at the top of the window, to install the font on your system.
""".format(path+"font.ttf"))


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

  def demo():
    sw, sh, r = 320,220, 45
    lx3, ly2 = [r,(sw-1)/2,sw-1-r], [r,sh-1-r]
    lx2=[(lx3[0]+lx3[1])/2,(lx3[1]+lx3[2])/2]

    for x in range(2): chromac(lx2[x], sh/2, r, -1, not(x)*-1, x*pi/4, x%2)
    for y in range(2):
      for x in range(3): chromac(lx3[x], ly2[y], r, not(y), x-1, (2+3*y+x)*pi/4, (x+y)%2)

  display_(demo)