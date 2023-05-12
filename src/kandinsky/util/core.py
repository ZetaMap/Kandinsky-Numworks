######### Imports #########
from os import environ, name

try: from tkinter import Tk
except ImportError as e:
  e.msg = "tkinter is not installed. "+("please reinstall python with complements modules" if name == "nt" else "install it with 'sudo apt install python3-tk'")
  raise

import warnings
warnings.filterwarnings('ignore', category=UserWarning) # Disable SDL warning 
try:
  import sdl2dll
  from sdl2.ext import init, quit as sdl_quit, ttf, image
  from sdl2._internal import prettywarn

  init()
  ttf._ttf_init()
  image._sdl_image_init()

except (ImportError, RuntimeError) as e:
  e.msg = """PySDL2 or PySDL2-dll module is not installed on your system, and kandinsky depend to it.
>>> To install, follow steps on the GitHub project: https://github.com/ZetaMap/Kandinsky-Numworks
>>> or type 'pip install -U pysdl2 pysdl2-dll"""
  raise

try: import ion
except ImportError: ION_PRESENT = False
else: 
  # In older version i forgot to define __version__ field
  # so if is not defined, is an outdated version.
  # Or verify if version is good
  if not hasattr(ion, "__version__") or tuple([int(i) for i in ion.__version__.split('.') if i.isdecimal()]) < (1, 2, 3):
    # idk why but warning don't print, so will show it manually
    print("ImportWarning: outdated version of 'Ion-numworks', please update it")
    ION_PRESENT = False

  # Another module is called ion, so do a little test to see if it's the right module
  else: ION_PRESENT = hasattr(ion, "keydown") 

from threading import Thread, main_thread
from math import sqrt
from .stuff import *


######### Environ config #########
DEBUG = 'KANDINSKY_ENABLE_DEBUG' in environ #or True 

NO_GUI = 'KANDINSKY_NO_GUI' in environ

# '0': PC, '1': Numworks, '2': Omega, '3': Upsilon
os = environ.get('KANDINSKY_OS_MODE')
if os and os.isdecimal(): Vars.selected_os = int(os) if 0 <= int(os) < len(Config.os_list) else Config.default_os

# '0': n0100, '1': n0110, '2': n0120
model = environ.get('KANDINSKY_MODEL_MODE')
if model and model.isdecimal(): Vars.selected_model = int(model) if 0 <= int(model) < len(Config.model_list) else Config.default_model

if 'KANDINSKY_SCREEN_SIZE' in environ:
  screen = environ['KANDINSKY_SCREEN_SIZE'].split('x')
  
  if len(screen) != 2: 
    raise \
      ValueError("invalid screen format. format to use: '<width>x<height>'")
  
  for i in range(2):
    if not screen[i].isdecimal() or int(screen[i]) < 0: 
      raise \
        ValueError("screen dimensions must be positive integers")
    screen[i] = int(screen[i])
    
  screen[1] -= Vars.head_size
  if screen[0] < Vars.screen[0] or screen[1] < Vars.screen[1]:
    raise \
      ValueError(f"screen dimensions must be greater than {Vars.screen[0]}x{Vars.screen[1]+Vars.head_size}")
  
  Vars.screen = tuple(screen)

zoom = environ.get('KANDINSKY_ZOOM_RATIO')
if zoom and zoom.isdecimal() and 1 <= int(zoom) <= Config.zoom_max: Vars.zoom_ratio = int(zoom)

# Experimental way to get more real emulation of numworks
import threading
USE_HEAP = 'KANDINSKY_USE_HEAP' in environ and hasattr(threading, "get_native_id")
# same problem than warning of ion
if USE_HEAP: print("ResourceWarning: python heap limitator is an experimental feature, so it can crach python several times")

######### Cleanup #########
del environ, name, os, model, zoom, init, sdl2dll, ttf, image, warnings, threading, #prettywarn


######### Main code #########
__all__ = ["Core"]

class Core(Thread): 
  stoped = False
  asknoclose = False
  OS_MODE = Config.default_os

  def __init__(self):
    Gui.paused = Gui.already_paused = True # Pause events to give the time of thread to initialize

    super().__init__(None, self.event_loop, Vars.app_name.replace(' ', '')+self.__class__.__name__)
    self.start()
    while Gui.paused and self.is_alive(): usleep(100) # Wait a little to synchronize it

  def quit_app(self, *_):
    if not self.stoped:
      self.stoped = True 
      Gui.paused = False # Now all calls of kandinsky raise an error

      Gui.destroy()
      sdl_quit()

  def print_debug(self, type, *messages, type_length=5, **args):
    if DEBUG: 
      print("DEBUG: ", end='')
      print(type+' '*(type_length-len(type))+':', *messages, **args)

  def verify(self, method, *args, **kwargs):
    self.print_debug("Event", " "+method.__name__, (*args, *[f"{k}={'v' if type(v) == str else v}" for k, v in kwargs.items()]), sep='')

    if Gui.paused: self.print_debug("Pause", "waiting...")
    while Gui.paused and self.is_alive(): usleep(1000)

    if self.stoped: raise RuntimeError("kandinsky window destroyed")
    elif not self.is_alive(): raise RuntimeError(f"an internal error has occurred. Stack trace is before this it.")

  def sleep(self, delay_us):
    if USE_HEAP and Gui.heap_set: return # No need to sleep

    ratio = Gui.data.model*Gui.data.ratio
    delay = int(delay_us*ratio)

    self.print_debug("Delay", "input =", delay_us, "µs, ratio ≃", str(round(ratio, 6))+", output =", delay, "µs")
    if ratio > 0: usleep(delay)

### methods
  def get_pixel(self, x, y):
    Tests.int(x, y)

    if y < 0 or y > Vars.screen[0] or x < 0 or x > Vars.screen[1]: color = Colors.black
    else: color = Colors.convert(Draw.get_at(Gui.drawable, x, y))

    self.sleep(77)
    return color

  def set_pixel(self, x, y, color):
    Tests.int(x, y)

    Draw.pixel(Gui.drawable, Colors.convert(color), x, y)
    self.sleep(130)

  def color(self, r, g, b):
    if g is None and b is None: color = Colors.convert(r)
    elif g is not None and b is not None: 
      Tests.int(r, g, b)
      color = Colors.convert((r, g, b))
    else: raise TypeError("color takes 1 or 3 arguments")

    self.sleep(100)
    return color

  def draw_string(self, text, x, y, color, background, font=False):
    Tests.str(text)
    Tests.int(x, y)
    
    color = Colors.convert(color)
    background = Colors.convert(background)
    bs = (7, 14) if font else (10,18)
    font = Config.small_font if font else Config.large_font
    if '\0' in text: text = text[:text.index('\0')]

    for i, l in enumerate(text.replace('\r', '').replace('\f', '\x01').replace('\b', '\x01').replace('\v', '\x01').replace('\t', "    ").splitlines()): 
      Draw.rect(Gui.drawable, background, (x*(not i), y+i*bs[1], len(l)*bs[0], bs[1]))
      Draw.string(Gui.drawable, font, l, x*(not i), y+i*bs[1]-2, color)
    self.sleep(86*(len(text)+(len(text)>=5)//1.2))
  
  def fill_rect(self, x, y, width, height, color):
    Tests.int(x, y, width, height)
  
    if width < 0:  x, width = x+width, -width
    if height < 0: y, height = y+height, -height
    
    Draw.rect(Gui.drawable, Colors.convert(color), (x, y, width, height))
    self.sleep(130+width*height/20+width*height*0.02)

  def wait_vblank(self):
    """why this?"""
    while not self.refreshed: usleep(100)

  def get_keys(self):
    """Don't tell me about this XD, it's omega"""
    # Raise an error if Ion-Numworks is not installed
    if not ION_PRESENT: raise NotImplementedError("please install or update the module 'Ion-numworks' before using this method")
    return ion.get_keys()

  def draw_line(self, x1, y1, x2, y2, color):
    """https://github.com/UpsilonNumworks/Upsilon/blob/upsilon-dev/kandinsky/src/context_line.cpp"""
    Tests.int(x1, y1, x2, y2)
    color = Colors.convert(color)

    s = abs(y2-y1) > abs(x2-x1)
    if s: x1, y1, x2, y2 = y1, x1, y2, x2
    if x1 > x2: x1, x2, y1, y2 = x2, x1, y2, y1
    g = 1 if x2 == x1 else (y2-y1)/(x2-x1)

    for x in range(x1, x2):
      ty = int(y1+g*(x-x1))
      Draw.pixel(Gui.drawable, color, *((ty, x) if s else (x, ty)))

    self.sleep(111) # TODO: calculate speed

  def draw_circle(self, x, y, r, color):
    """https://github.com/UpsilonNumworks/Upsilon/blob/upsilon-dev/kandinsky/src/context_circle.cpp"""
    Tests.int(x, y, r)
    
    color = Colors.convert(color)
    xc, yc, m = 0, abs(r), 5-4*abs(r) 

    while xc <= yc:
      Draw.pixel(Gui.drawable, color, xc+x, yc+y)
      Draw.pixel(Gui.drawable, color, yc+x, xc+y)
      Draw.pixel(Gui.drawable, color, -xc+x, yc+y)
      Draw.pixel(Gui.drawable, color, -yc+x, xc+y)
      Draw.pixel(Gui.drawable, color, xc+x, -yc+y)
      Draw.pixel(Gui.drawable, color, yc+x, -xc+y)
      Draw.pixel(Gui.drawable, color, -xc+x, -yc+y)
      Draw.pixel(Gui.drawable, color, -yc+x, -xc+y)
      
      if m > 0: yc, m = yc-1, m-8*yc
      xc, m = xc+1, m+8*xc+4 

    self.sleep(222) # TODO: calculate speed

  def fill_circle(self, x, y, r, color):
    """https://github.com/UpsilonNumworks/Upsilon/blob/upsilon-dev/kandinsky/src/context_circle.cpp"""
    Tests.int(x, y, r)
    color = Colors.convert(color)

    r = abs(r)
    for i in range(x-r, x+r):
      semi = int(sqrt(r**2-(x-i)**2))
      Draw.rect(Gui.drawable, color, (i, y-semi, 1, semi*2))

    self.sleep(333) # TODO: calculate speed

  def fill_polygon(self, points, color):
    """https://github.com/UpsilonNumworks/Upsilon/blob/upsilon-dev/kandinsky/src/context_polygon.cpp"""
    Tests.list(points)
    if len(points) < 3: raise ValueError("polygon must have least 3 points")
    tests = [[len(i) for v in i if len(i) != 2 or not Tests.int(v)] for i in points if Tests.list(i)]
    if len(tests) and len(tests[0]): raise ValueError("requested length 2 but object has length "+str(tests[0][0]))
    
    color = Colors.convert(color)
    points_size = len(points)

    for y in range(min([0,Vars.screen[0]]+points, key=lambda v: v[1]), max([0,0]+points, key=lambda v: v[1])):
      switches = []
      last_point = points_size-1

      for i in range(points_size):
        point_y, last_point_y = points[i][1], points[last_point][1]
        if ((point_y < y and last_point_y >= y) or (last_point_y < y and point_y >= y)) and point_y != last_point_y:
          switches.append(round(points[i][0]+1*(y-point_y)/(last_point_y-point_y)*(points[last_point][0]-points[i][0])))
        last_point = i

      switches.sort()
      for x in range(0, len(switches), 2):
        if switches[x] >= Vars.screen[1]*2: break
        if switches[x+1] > 0: Draw.rect(Gui.drawable, color, (switches[x], y, switches[x+1]-switches[x], 1))

    self.sleep(444) # TODO: calculate speed

  def get_palette():
    return {"Toolbar":        Gui.data.color, 
            "AccentText":     (0, 132, 120), 
            "HomeBackground": Colors.white, 
            "PrimaryText":    Colors.black,
            "SecondaryText":  (104, 108, 104)}
###

  def event_loop(self):
    root = Tk()
    if USE_HEAP: Gui._main_thread_pid = self.native_id
    
    try:
      Gui(root)
      Gui.config(not NO_GUI)
    except RuntimeError as e:
      # Handle multiple import of library
      # Library cannot open new tkinter root windows while another is opened but it can open another if previous is destroyed
      # Note: no data from the previous window can be restored to new one
      if "main thread is not in main loop" in e.args[0]: prettywarn("multiple creation of window is not permitted", ImportWarning)
      else: self.print_debug("ERROR", type(e).__name__+": "+e.args[0])
      return

    self.OS_MODE = Gui.os_mode.get()
    # Bind more event
    root.protocol("WM_DELETE_WINDOW", self.quit_app)
    root.bind("<Control-q>", self.quit_app)

    Gui.paused = Gui.already_paused = False # Initialization finished, unpause events

    while True:
      if self.stoped:
        self.quit_app() 
        return  
      elif not self.asknoclose and not main_thread().is_alive():
        if Gui.askscriptend(): self.stoped = True
        else: self.asknoclose = True
      
      self.refreshed = False
      try: Gui.refresh()
      except AttributeError: pass
      except RuntimeError: self.stoped = True
      usleep(1000)
      self.refreshed = True

  def event_fire(self, method, *arg, **kwargs):
    try: 
      self.verify(method, *arg, **kwargs)
      return method(*arg, **kwargs), None
    except (Exception, BaseException) as e: 
      return None, Exception.with_traceback(
        KeyboardInterrupt(type(e).__name__+": "+' '.join(e.args)) if isinstance(e, RuntimeError) else e, 
        e.__traceback__.tb_next if DEBUG else None)
