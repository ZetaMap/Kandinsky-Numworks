######### Environ config #########
from os import environ

DEBUG = 'KANDINSKY_ENABLE_DEBUG' in environ #or True 

NO_GUI = 'KANDINSKY_NO_GUI' in environ

DEFAULT_OS = 1
try: START_OS = int(environ.get('KANDINDKY_START_OS', DEFAULT_OS)) # '0': PC, '1': Numworks, '2': Omega, '3': Upsilon
except ValueError: START_OS = DEFAULT_OS

DEFAULT_MODEL = 1
try: START_MODEL = int(environ.get('KANDINDKY_START_MODEL', DEFAULT_MODEL)) # '0': n0100, '1': n0110, '2': n0120
except ValueError: START_MODEL = DEFAULT_MODEL


######### Init #########
import warnings
warnings.filterwarnings('ignore', category=UserWarning) # Disable SDL warning 
try: 
  import sdl2
  import sdl2.ext

  sdl2.ext.init()
  sdl2.ext.image._sdl_image_init()

except ImportError as e:
  e.args = ("""
>>> PySDL2 or PySDL2-dll module is not installed on your system, and kandinsky depend to it.
>>> To install it follow steps on the GitHub project: https://github.com/ZetaMap/Kandinsky-Numworks""",)
  raise

# Cleanup namespaces
del environ, sdl2, warnings


######### Imports #########
from tkinter import Tk
from sdl2 import SDL_Delay
from sdl2.ext import quit as sdl_quit
from threading import Thread
from random import randint

# Internal libraries
from .stuff import *
from .time.GS_timing import micros


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
    self.stoped = True 
    self.paused = False # Now all calls of kandinsky raise an error
    
    Gui.header.close()
    Gui.screen.close()
    sdl_quit()
    self.root.quit()

  def print_debug(self, type, *messages, type_length=5, **args):
    if DEBUG: print("DEBUG:", type+' '*(type_length-len(type))+':', *messages, **args)

  def verify(self, method, *args, **kwargs):

    self.print_debug("Event", method.__name__, (*args, *[f"{k}={'v' if type(v) == str else v}" for k, v in kwargs.items()]))

    if Gui.paused: self.print_debug("Pause", "waiting...")
    while Gui.paused and self.is_alive(): SDL_Delay(10)

    if self.stoped: raise RuntimeError("kandinsky window destroyed")
    elif not self.is_alive(): raise RuntimeError(f"an error has occurred in thread '{self.name}'")
    
    self.time = micros()

  def sleep(self, delay_us):
    ratio = Gui.data.model*Gui.data.ratio*(randint(900, 1100)/1000) # multiplie random ratio between 0.9 and 1.1 to simulate speed of python
    delay = delay_us*ratio//1

    self.print_debug("Delay", "input =", delay_us, "µs, ratio ≃", str(round(ratio, 6))+", output =", delay, "µs")
    while micros()-self.time < delay: pass

  def int_test(self, *objects):
    err = [type(i).__name__ for i in objects if type(i) != int]
    if len(err) > 0: raise TypeError(f"can't convert {err[0]} to int")

  def get_pixel(self, x, y):
    self.int_test(x, y)

    if y < 0 or x < 0: color = Colors.black
    else: color = Colors.convert(Draw.get_at(self.drawable, x, y))

    self.sleep(77)
    return color

  def set_pixel(self, x, y, color):
    self.int_test(x, y)

    Draw.pixel(self.drawable, Colors.convert(color), x, y)
    self.sleep(130)

  def color(self, r, g, b):
    if not g and not b: color = Colors.convert(r)
    elif g and b: 
      self.int_test(r, g, b)
      color = Colors.convert((r, g, b))
    else: raise TypeError("color takes 1 or 3 arguments")

    self.sleep(100)
    return color

  def _drawString(self, text, x, y, color, background):
    Draw.rect(self.drawable, background, (x, y, len(text)*10, 18))
    Draw.blit(self.drawable, Config.large_font.render(text, color=color), (x, y-2))

  def draw_string(self, text, x, y, color, background):
    if type(text) != str: raise TypeError(f"can't convert '{type(text).__name__}' object to str implicitly")
    self.int_test(x, y)
    
    color = Colors.convert(color)
    background = Colors.convert(background)
    stext = len(text)
    text = text.replace('\t', "    ").splitlines()

    self._drawString(text[0], x, y, color, background)
    for i in range(1, len(text)): self._drawString(text[i], 0, y+i*18, color, background)
    self.sleep(86*(stext+(stext>=5)//1.2))
  
  def fill_rect(self, x, y, width, height, color):
    self.int_test(x, y, width, height)
  
    if width < 0:  x, width = x+width, -width
    if height < 0: y, height = y+height, -height
    
    Draw.rect(Gui.screen.get_surface(), Colors.convert(color), (x, y, width, height))
    self.sleep(130+width*height/20+width*height*0.02)

  def event_loop(self):
    self.root = Tk()

    Gui(self.root, (START_OS, DEFAULT_OS), (START_MODEL, DEFAULT_MODEL))
    Gui.config(NO_GUI)
    self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    # Get drawable surface and default color
    self.drawable = Gui.screen.get_surface()
    Draw.rect(self.drawable, Colors.black, (0, 0, Constants.screen[0], Constants.head_size))
    Draw.rect(self.drawable, Colors.white, (0, 0, *Constants.screen))

    Gui.paused = False # Initialization finished, unpause events

    while True:
      if self.stoped:
        self.quit_app() 
        return  
      
      Gui.header.refresh()
      Gui.screen.refresh()  
      self.root.update_idletasks()  
      self.root.update()
      Gui.header_frame.update()
      Gui.screen_frame.update()

      SDL_Delay(60)# Not exactly 60 FPS

  def event_fire(self, method, *arg, **kwargs):
    try: 
      self.verify(method, *arg, **kwargs)
      return method(*arg, **kwargs), None
    except (Exception, BaseException) as e: 
      return None, Exception.with_traceback(KeyboardInterrupt(type(e).__name__+": "+e.args[0]) if isinstance(e, BaseException) else e, 
                                            e.__traceback__.tb_next if DEBUG else None)
