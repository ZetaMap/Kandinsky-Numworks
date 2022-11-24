######### Environ config #########
import os

DEBUG = 'KANDINSKY_ENABLE_DEBUG' in os.environ #or True 

NO_GUI = 'KANDINSKY_NO_GUI' in os.environ

DEFAULT_OS = 1
# '0': PC, '1': Numworks, '2': Omega, '3': Upsilon
try: OS_MODE = int(os.environ.get('KANDINSKY_OS_MODE', DEFAULT_OS)) 
except ValueError: OS_MODE = DEFAULT_OS

DEFAULT_MODEL = 1
# '0': n0100, '1': n0110, '2': n0120
try: MODEL_MODE = int(os.environ.get('KANDINSKY_MODEL_MODE', DEFAULT_MODEL))
except ValueError: MODEL_MODE = DEFAULT_MODEL


######### Init #########
import warnings
warnings.filterwarnings('ignore', category=UserWarning) # Disable SDL warning 
try:
  import sdl2
  import sdl2.ext

  sdl2.ext.init()
  sdl2.ext.ttf._ttf_init()
  sdl2.ext.image._sdl_image_init()

except ImportError as e:
  e.args = ("""PySDL2 or PySDL2-dll module is not installed on your system, and kandinsky depend to it.
>>> To install it follow steps on the GitHub project: https://github.com/ZetaMap/Kandinsky-Numworks
>>> or type 'pip install pysdl2 pysdl2-dll""",)
  raise

try: import tkinter
except ImportError as e:
  e.args = ("tkinter is not installed. "+("please reinstall python with complements modules" if os.name == "nt" else "install it with 'sudo apt install python3-tk'"),)
  raise

# Cleanup namespaces
del os, sdl2, tkinter, warnings


__all__ = [
  "Core",
  "OS_MODE",
  "DEFAULT_OS",
  "MODEL_MODE"
  "DEFAULT_MODE",
  "NO_GUI"
]

######### Imports #########
from tkinter import Tk
from sdl2 import SDL_Delay
from sdl2.ext import quit as sdl_quit
from threading import Thread
from random import randint
from time import monotonic_ns
from math import sqrt
from .stuff import *


######### Main code #########
class Core(Thread): 
  stoped = False
  drawable = None

  def __init__(self):
    Gui.paused = True # Pause events to give the time of thread to initialize

    super().__init__(None, self.event_loop, Constants.app_name.replace(' ', '')+self.__class__.__name__)
    self.start()
    while Gui.paused and self.is_alive(): pass # Wait a little to synchronize it

  def quit_app(self):
    if not self.stoped:
      self.stoped = True 
      self.paused = False # Now all calls of kandinsky raise an error

      Gui.head.close()
      Gui.screen.close()
      
      sdl_quit()
      self.root.quit()

  def print_debug(self, type, *messages, type_length=5, **args):
    if DEBUG: 
      print("DEBUG: ", end='')
      print(type+' '*(type_length-len(type))+':', *messages, **args)

  def verify(self, method, *args, **kwargs):
    self.print_debug("Event", " "+method.__name__, (*args, *[f"{k}={'v' if type(v) == str else v}" for k, v in kwargs.items()]), sep='')

    if Gui.paused: self.print_debug("Pause", "waiting...")
    while Gui.paused and self.is_alive(): SDL_Delay(1)

    if self.stoped: raise RuntimeError("kandinsky window destroyed")
    elif not self.is_alive(): raise RuntimeError(f"an error has occurred in thread '{self.name}'")
    
    self.time = monotonic_ns()//1000

  def sleep(self, delay_us):
    ratio = Gui.data.model*Gui.data.ratio*(randint(900, 1100)/1000) # multiplie random ratio between 0.9 and 1.1 to simulate speed of python
    delay = delay_us*ratio//1

    self.print_debug("Delay", "input =", delay_us, "µs, ratio ≃", str(round(ratio, 6))+", output =", delay, "µs")
    while monotonic_ns()//1000-self.time < delay: pass

### methods when used
  def get_pixel(self, x, y):
    Tests.int_test(x, y)

    if y < 0 or y > Constants.screen[0] or x < 0 or x > Constants.screen[1]: color = Colors.black
    else: color = Colors.convert(Draw.get_at(self.drawable, x, y))

    self.sleep(77)
    return color

  def set_pixel(self, x, y, color):
    Tests.int_test(x, y)

    Draw.pixel(self.drawable, Colors.convert(color), x, y)
    self.sleep(130)

  def color(self, r, g, b):
    if not g and not b: color = Colors.convert(r)
    elif g and b: 
      Tests.int_test(r, g, b)
      color = Colors.convert((r, g, b))
    else: raise TypeError("color takes 1 or 3 arguments")

    self.sleep(100)
    return color

  def _drawString(self, text, x, y, color, background):
    Draw.rect(self.drawable, background, (x, y, len(text)*10, 18))
    Draw.blit(self.drawable, Config.font.render(text, color=color), (x, y-2))

  def draw_string(self, text, x, y, color, background, font=False):
    Tests.str_test(text)
    Tests.int_test(x, y)
    
    color = Colors.convert(color)
    background = Colors.convert(background)
    stext = len(text)
    text = text.replace('\t', "    ").splitlines()

    self._drawString(text[0], x, y, color, background)
    for i in range(1, len(text)): self._drawString(text[i], 0, y+i*18, color, background)
    self.sleep(86*(stext+(stext>=5)//1.2))
  
  def fill_rect(self, x, y, width, height, color):
    Tests.int_test(x, y, width, height)
  
    if width < 0:  x, width = x+width, -width
    if height < 0: y, height = y+height, -height
    
    Draw.rect(self.drawable, Colors.convert(color), (x, y, width, height))
    self.sleep(130+width*height/20+width*height*0.02)

  def wait_vblank(self):
    """why this?"""
    while not self.refreshed: pass

  def get_keys(self):
    """Don't tell me about this XD, it's omega"""
    return Ion.get_keys()

  def draw_line(self, x1, y1, x2, y2, color):
    """https://github.com/UpsilonNumworks/Upsilon/blob/upsilon-dev/kandinsky/src/context_line.cpp"""
    Tests.int_test(x1, y1, x2, y2)
    color = Colors.convert(color)

    s = abs(y2-y1) > abs(x2-x1)
    if s: x1, y1, x2, y2 = y1, x1, y2, x2
    if x1 > x2: x1, x2, y1, y2 = x2, x1, y2, y1
    g = 1 if x2 == x1 else (y2-y1)/(x2-x1)

    for x in range(x1, x2):
      ty = int(y1+g*(x-x1))
      Draw.pixel(self.drawable, color, *((ty, x) if s else (x, ty)))

    self.sleep(111) # TODO: calculate speed

  def draw_circle(self, x, y, r, color):
    """https://github.com/UpsilonNumworks/Upsilon/blob/upsilon-dev/kandinsky/src/context_circle.cpp"""
    Tests.int_test(x, y, r)
    
    color = Colors.convert(color)
    xc, yc, m = 0, abs(r), 5-4*abs(r) 

    while xc <= yc:
      Draw.pixel(self.drawable, color, xc+x, yc+y)
      Draw.pixel(self.drawable, color, yc+x, xc+y)
      Draw.pixel(self.drawable, color, -xc+x, yc+y)
      Draw.pixel(self.drawable, color, -yc+x, xc+y)
      Draw.pixel(self.drawable, color, xc+x, -yc+y)
      Draw.pixel(self.drawable, color, yc+x, -xc+y)
      Draw.pixel(self.drawable, color, -xc+x, -yc+y)
      Draw.pixel(self.drawable, color, -yc+x, -xc+y)
      
      if m > 0: yc, m = yc-1, m-8*yc
      xc, m = xc+1, m+8*xc+4 

    self.sleep(222) # TODO: calculate speed

  def fill_circle(self, x, y, r, color):
    """https://github.com/UpsilonNumworks/Upsilon/blob/upsilon-dev/kandinsky/src/context_circle.cpp"""
    Tests.int_test(x, y, r)
    color = Colors.convert(color)

    r = abs(r)
    for i in range(x-r, x+r):
      semi = int(sqrt(r**2-(x-i)**2))
      Draw.rect(self.drawable, color, (i, y-semi, 1, semi*2))

    self.sleep(333) # TODO: calculate speed

  def fill_polygon(self, points, color):
    """https://github.com/UpsilonNumworks/Upsilon/blob/upsilon-dev/kandinsky/src/context_polygon.cpp"""
    Tests.list_test(points)
    if len(points) < 3: raise ValueError("polygon must have least 3 points")
    tests = [[len(i) for v in i if len(i) != 2 or not Tests.int_test(v)] for i in points if Tests.list_test(i)]
    if len(tests) and len(tests[0]): raise ValueError("requested length 2 but object has length "+str(tests[0][0]))
    color = Colors.convert(color)

    top, bottom = Constants.screen[0], 0
    points_size = len(points)

    # find top of polygon
    for _, p in points:
      if p < top: top = p
      if p > bottom: bottom = p

    for y in range(top, bottom):
      switches = []
      last_point = points_size-1

      for i in range(points_size):
        point_y, last_point_y = points[i][1], points[last_point][1]
        if ((point_y < y and last_point_y >= y) or (last_point_y < y and point_y >= y)) and point_y != last_point_y:
          switches.append(round(points[i][0]+1*(y-point_y)/(last_point_y-point_y)*(points[last_point][0]-points[i][0])))
        last_point = i

      switches.sort()
      for x in range(0, len(switches), 2):
        point_x = switches[x]
        if switches[x] >= Constants.screen[1]*2: break
        if switches[x+1] > 0: Draw.rect(self.drawable, color, (point_x, y, switches[x+1]-point_x, 1))

    self.sleep(444) # TODO: calculate speed

  def get_palette():
    return {"Toolbar":        Colors.convert(Gui.data.color), 
            "AccentText":     (0, 132, 120), 
            "HomeBackground": Colors.white, 
            "PrimaryText":    Colors.black,
            "SecondaryText":  (104, 108, 104)}
###

  def event_loop(self):
    self.root = Tk()

    Gui(self.root, (OS_MODE, DEFAULT_OS), (MODEL_MODE, DEFAULT_MODEL))
    Gui.config(NO_GUI)
    self.OS_MODE = Gui.os_mode.get()
    self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    # Set surfaces
    self.drawable = Gui.screen.get_surface()
    Draw.rect(self.drawable, Colors.white)
    Gui.update_data()

    Gui.paused = False # Initialization finished, unpause events

    while True:
      if self.stoped:
        self.quit_app() 
        return  
      
      self.refreshed = False
      Gui.head.refresh()
      Gui.screen.refresh()
      try: Gui.refresh()
      except AttributeError: pass
      SDL_Delay(1)
      self.refreshed = True

  def event_fire(self, method, *arg, **kwargs):
    try: 
      self.verify(method, *arg, **kwargs)
      return method(*arg, **kwargs), None
    except (Exception, BaseException) as e: 
      return None, Exception.with_traceback(KeyboardInterrupt(type(e).__name__+": "+e.args[0]) if isinstance(e, BaseException) else e, 
                                            e.__traceback__.tb_next if DEBUG else None)


######### Register to end of script #########
...