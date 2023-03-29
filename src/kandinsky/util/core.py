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

except (ImportError, ModuleNotFoundError) as e:
  e.args = ("""PySDL2 or PySDL2-dll module is not installed on your system, and kandinsky depend to it.
>>> To install, follow steps on the GitHub project: https://github.com/ZetaMap/Kandinsky-Numworks
>>> or type 'pip install pysdl2 pysdl2-dll""",)
  raise

try: import tkinter
except (ImportError, ModuleNotFoundError) as e:
  e.args = ("tkinter is not installed. "+("please reinstall python with complements modules" if os.name == "nt" else "install it with 'sudo apt install python3-tk'"),)
  raise

try: import ion
except (ImportError, ModuleNotFoundError): ION_PRESENT = False
else: 
  # In older version i forgot to define __version__ field
  # so if is not defined, is an outdated version
  if not hasattr(ion, "__version__") : ION_PRESENT = False
  
  # Verify if version is good
  elif tuple([int(i) for i in ion.__version__.split('.') if i.isdecimal()]) < (1, 2, 3):
    sdl2._internal.prettywarn("outdated version of 'Ion-numworks', please update it", ImportWarning)
    ION_PRESENT = False

  # Another module is called ion, so do a little test to see if it's the right module
  else: ION_PRESENT = hasattr(ion, "keydown") 

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
from sdl2.ext import quit as sdl_quit
from threading import Thread, main_thread
from math import sqrt
from .stuff import *

# Try to find an real time clock to do microseconds sleeps
if Constants.is_windows:
  # Try to use module win-precise-time to get more sleeps precision
  try:
    import win_precise_time as _wpt
    usleep = lambda us: _wpt.sleep_until_ns(int(_wpt.time_ns()+us*1000))
  except:
    import time as _time, sdl2._internal
    sdl2._internal.prettywarn("win-precise-time module is not installed. Using time module to do usleep (emulation will be less accurate)", RuntimeWarning)
    def usleep(us):
      t = _time.perf_counter_ns()+us*1000
      while _time.perf_counter_ns() < t: _time.sleep(1e-9)
    del sdl2._internal
else:
  try:
    import ctypes
    usleep = ctypes.CDLL("libc.so.6").usleep
    del ctypes
  except:
    # On some linux distribution, this library is not installed by default
    import time as _time, sdl2._internal
    sdl2._internal.prettywarn("libc6 library is not installed. Using time module to do usleep (emulation will be less accurate)", RuntimeWarning)
    usleep = lambda us: _time.sleep(us/10e6)
    del sdl2._internal


######### Main code #########
class Core(Thread): 
  stoped = False
  drawable = None
  asknoclose = False

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
    while Gui.paused and self.is_alive(): usleep(1000)

    if self.stoped: raise RuntimeError("kandinsky window destroyed")
    elif not self.is_alive(): raise RuntimeError(f"an internal error has occurred. Stack trace is before this it.")

  def sleep(self, delay_us):
    ratio = Gui.data.model*Gui.data.ratio
    delay = int(delay_us*ratio)

    self.print_debug("Delay", "input =", delay_us, "µs, ratio ≃", str(round(ratio, 6))+", output =", delay, "µs")
    if ratio > 0: usleep(delay)

### methods when used
  def get_pixel(self, x, y):
    Tests.int(x, y)

    if y < 0 or y > Constants.screen[0] or x < 0 or x > Constants.screen[1]: color = Colors.black
    else: color = Colors.convert(Draw.get_at(self.drawable, x, y))

    self.sleep(77)
    return color

  def set_pixel(self, x, y, color):
    Tests.int(x, y)

    Draw.pixel(self.drawable, Colors.convert(color), x, y)
    self.sleep(130)

  def color(self, r, g, b):
    if not g and not b: color = Colors.convert(r)
    elif g and b: 
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
      Draw.rect(self.drawable, background, (x*(not i), y+i*bs[1], len(l)*bs[0], bs[1]))
      Draw.blit(self.drawable, font.render(l, color=color), (x*(not i), y+i*bs[1]-2))
    self.sleep(86*(len(text)+(len(text)>=5)//1.2))
  
  def fill_rect(self, x, y, width, height, color):
    Tests.int(x, y, width, height)
  
    if width < 0:  x, width = x+width, -width
    if height < 0: y, height = y+height, -height
    
    Draw.rect(self.drawable, Colors.convert(color), (x, y, width, height))
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
      Draw.pixel(self.drawable, color, *((ty, x) if s else (x, ty)))

    self.sleep(111) # TODO: calculate speed

  def draw_circle(self, x, y, r, color):
    """https://github.com/UpsilonNumworks/Upsilon/blob/upsilon-dev/kandinsky/src/context_circle.cpp"""
    Tests.int(x, y, r)
    
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
    Tests.int(x, y, r)
    color = Colors.convert(color)

    r = abs(r)
    for i in range(x-r, x+r):
      semi = int(sqrt(r**2-(x-i)**2))
      Draw.rect(self.drawable, color, (i, y-semi, 1, semi*2))

    self.sleep(333) # TODO: calculate speed

  def fill_polygon(self, points, color):
    """https://github.com/UpsilonNumworks/Upsilon/blob/upsilon-dev/kandinsky/src/context_polygon.cpp"""
    Tests.list(points)
    if len(points) < 3: raise ValueError("polygon must have least 3 points")
    tests = [[len(i) for v in i if len(i) != 2 or not Tests.int(v)] for i in points if Tests.list(i)]
    if len(tests) and len(tests[0]): raise ValueError("requested length 2 but object has length "+str(tests[0][0]))
    
    color = Colors.convert(color)
    points_size = len(points)

    for y in range(min([0,Constants.screen[0]]+points, key=lambda v: v[1]), max([0,0]+points, key=lambda v: v[1])):
      switches = []
      last_point = points_size-1

      for i in range(points_size):
        point_y, last_point_y = points[i][1], points[last_point][1]
        if ((point_y < y and last_point_y >= y) or (last_point_y < y and point_y >= y)) and point_y != last_point_y:
          switches.append(round(points[i][0]+1*(y-point_y)/(last_point_y-point_y)*(points[last_point][0]-points[i][0])))
        last_point = i

      switches.sort()
      for x in range(0, len(switches), 2):
        if switches[x] >= Constants.screen[1]*2: break
        if switches[x+1] > 0: Draw.rect(self.drawable, color, (switches[x], y, switches[x+1]-switches[x], 1))

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
    
    try:
      Gui(self.root, (OS_MODE, DEFAULT_OS), (MODEL_MODE, DEFAULT_MODEL))
      Gui.config(NO_GUI)
      self.OS_MODE = Gui.os_mode.get()
      self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
    except RuntimeError as e:
      # Handle multiple import of library
      # Library cannot open new tkinter root windows while another is opened but it can open another if previous is destroyed
      # Note: no data from the previous window can be restored to new one
      if "main thread is not in main loop" in e.args:
        import warnings
        warnings.warn("multiple creation of window is not permitted", ImportWarning)
        del warnings
      else: self.print_debug("ERROR", type(e).__name__+": "+e.args[0])
      return
      
    # Set surfaces
    self.drawable = Gui.screen.get_surface()
    Draw.rect(self.drawable, Colors.white)
    Gui.update_data()

    Gui.paused = False # Initialization finished, unpause events

    while True:
      if self.stoped:
        self.quit_app() 
        return  
      elif not self.asknoclose and not main_thread().is_alive():
        if Gui.askscriptend(): self.stoped = True
        else: self.asknoclose = True
      
      self.refreshed = False
      Gui.head.refresh()
      Gui.screen.refresh()
      try: Gui.refresh()
      except AttributeError: pass
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
