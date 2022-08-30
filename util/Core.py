######### Dependencies #########

from os import environ, getcwd
# Remove pygame header
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''

# Debug pre-select
DEBUG = 'KANDINSKY_ENABLE_DEBUG' in environ #or True 

# '0': PC, '1': Numworks, '2': Omega, '3': Upsilon
DEFAULT_OS = 1
START_OS = int(environ.get('KANDINDKY_START_OS', DEFAULT_OS))

# '0': n0100, '1': n0110, '2': n0120
DEFAULT_MODEL = 1
START_MODEL = int(environ.get('KANDINDKY_START_MODEL', DEFAULT_MODEL))
del environ

try: import pygame
except ImportError: raise ImportError("""
>>> Pygame module is not installed on your system, and kandinsky depend to it.
To install Pygame follow steps on the GitHub project: https://github.com/ZetaMap/Kandinsky-Numworks""")
finally: del pygame

######### Imports #########

from pygame import display as screen, draw, event, key, init as pygame_init, image, error
from pygame.constants import QUIT, KEYDOWN, KMOD_CTRL, K_o, K_m, K_p, K_s
from threading import Thread
from random import randint
from datetime import datetime

# Internal libraries
from .vars import *
from .time.GS_timing import micros
from .gui import const

######### Main code #########

pygame_init()
Gui(Vars.path, (START_OS, DEFAULT_OS), (START_MODEL, DEFAULT_MODEL))
Fonts()
Vars()

class Core: 
  stoped = False
  screen_save = None

  def __init__(self):
    self.window = Thread(None, self.event_loop, Vars.app_name.replace(' ', '')+self.__class__.__name__)
    screen.set_caption(Vars.app_name)
    screen.set_icon(Vars.app_icon)
    self.window.start()

  def print_debug(self, type, *messages, type_length=12, **args):
    if DEBUG: print("DEBUG:", '['+type+' '*(type_length-len(type))+']', *messages, **args)

  def verify(self, method, *args, **kwargs):

    self.print_debug("Event/Method", method.__name__, (*args, *[k+'='+("'"+v+"'" if type(v) == str else str(v)) for k, v in kwargs.items()]))

    if Gui.state.paused: self.print_debug("Sleep/Paused", "waiting...")
    while Gui.state.paused and self.window.is_alive(): Vars.clock.tick(30)

    if self.stoped: raise RuntimeError("kandinsky window destroyed")
    elif not self.window.is_alive(): raise RuntimeError("an error has occurred in '"+self.window.name+"-Thread'")
    
    self.time = micros()

  def sleep(self, delay_us):
    delay = delay_us*Gui.model.ratio*Gui.mode.ratio*(randint(900, 1100)/1000)//1
    self.print_debug("Sleep/Delay", "input =", delay_us, "µs; output =", delay, "µn")
    while micros()-self.time < delay: pass

  def draw_header(self):
    draw.line(self.root, Colors.black, (0, Gui.height), (Vars.screen[0], Gui.height))
    draw.rect(self.root, Gui.mode.color, (0, Gui.height+1, Vars.screen[0], 18))
    self.root.blit(Fonts.small.render(Gui.mode.unit, True, Colors.white), (5, Gui.height+1))
    self.root.blit(Fonts.small.render("PYTHON", True, Colors.white), (Vars.screen[0]-181, Gui.height+2))
    x = Vars.screen[0]-20  
    if Gui.mode.clock: 
      self.root.blit(Fonts.small.render("12:00", True, Colors.white), (x-20, Gui.height+2))
      x -= 40
    draw.line(self.root, Colors.white, (x, Gui.height+6), (x, Gui.height+13))
    draw.rect(self.root, Colors.white, (x+2, Gui.height+6, 10, 8))
    draw.line(self.root, Colors.white, (x+13,Gui.height+ 6), (x+13, Gui.height+13))
    draw.line(self.root, Colors.white, (x+14, Gui.height+8), (x+14, Gui.height+11))
    

  def get_pixel(self, x, y):
    Errors.type_test(int, x, y)

    if y < 0 or x < 0 or x >= Vars.screen[0] or y+Vars.top_size >= Vars.screen[1]: color = Colors.black
    else: color = self.convert_color(self.root.get_at((x, y+Vars.top_size))[:-1])

    self.sleep(77)
    return color

  def set_pixel(self, x, y, color):
    Errors.type_test(int, x, y)

    if y > 0: self.root.set_at((x, y+Vars.top_size), self.convert_color(color))
    self.sleep(130)

  def color(self, r, g, b):
    if g == None and b == None: color = self.convert_color(r)
    elif g != None and b != None: 
      Errors.type_test(int, r, g, b)
      color = self.convert_color((r, g, b))
    else: raise TypeError("color takes 1 or 3 arguments")

    self.sleep(100)
    return color

  def drawString(self, text, x, y, color, background):
    draw.rect(self.root, self.convert_color(background), (x, y+2, len(text)*10, 18))
    self.root.blit(Fonts.large.render(text, True, self.convert_color(color)), (x, y))

  def draw_string(self, text, x, y, color, background):
    Errors.type_test(str, text)
    Errors.type_test(int, x, y)
    
    y += Vars.top_size-2
    if y > Gui.height:
      stext, text = len(text), text.replace('\r', '').replace('\t', "    ").split('\n')
      
      self.drawString(text[0], x, y, color, background)
      for i in range(1, len(text)): self.drawString(text[i], 0, y+i*18, color, background)
      if y < Vars.top_size: self.draw_header()

    self.sleep(86*(stext+(stext>=5)//1.2))
  
  def fill_rect(self, x, y, width, height, color):
    Errors.type_test(int, x, y, width, height)
  
    if width < 0:  x, width = x+width, -width
    if height < 0: y, height = y+height, -height
    if y < 0 and y+height > 0: height, y = height-y, 0
    
    if y+height > 0: draw.rect(self.root, self.convert_color(color), (x, y+Vars.top_size, width, height))
    self.sleep(130+width*height/20+width*height*0.02)

  def convert_color(self, color):
    Errors.type_test(Colors, Colors(color))
    
    color = Colors.get(color)
    return 0 if color[0] < 1 else color[0]%256//8*8, 0 if color[1] < 1 else color[1]%256//8*8, 0 if color[2] < 1 else color[2]%256//8*8
    
  def event_loop(self):
    self.root = screen.set_mode(Vars.screen)
    Gui.app.init(Gui.menu, self.root)

    # Register more events
    Gui.menu.find("mode").connect(const.CHANGE, self.draw_header)

    # Draw header
    self.root.fill(Colors.white)
    self.draw_header()
    Gui.state.paused = False # Initialization finished, unpause events

    # Thread loop
    while True:
      for e in event.get():
        if e.type == QUIT or self.stoped:
          self.stoped = True
          Gui.state.paused = False # Unpause event to raise error if continue to draw
          Vars.clock.tick(24) # Wait a little to avoid a 'Fatal Python error' from pygame parachute
          screen.quit()
          Gui.app.quit() 
          return # Stop the loop, so end Thread

        elif Gui.popup.is_hidden() and e.type == KEYDOWN and key.get_mods() & KMOD_CTRL: 
          pressed = key.get_pressed()
          if pressed[K_o]: 
            Gui.move_focus("mode-menu", Gui.mode.get("focus", None))
            self.print_debug("Event/Button", "Gui.mode :", Gui.mode)
          
          elif pressed[K_m]: 
            Gui.move_focus("model-menu", Gui.model.get("focus", None))
            self.print_debug("Event/Button", "Gui.model:", Gui.model)
          
          elif pressed[K_p]: 
            Gui.move_focus("state")
            self.print_debug("Event/Button", "Gui.state:", Gui.state)
            
          elif pressed[K_s]:
            # Take a screenshot and show popup for 3s
            if Gui.state.paused: Gui.state.already_paused = True
            Gui.state.paused = True # pause event, is more simple to implement a popup window
            for w in Gui.menu.widgets: w._close()
            file_path = getcwd()+Vars.dirchar
            file_name = datetime.now().strftime("Screenshot_%m-%d-%Y_%H-%M-%S.png")
            Gui.popup.set_content(file_path+file_name, file_path)
            try: image.save(self.root.subsurface((0, Gui.height, Vars.screen[0], Vars.screen[1]-Gui.height)), file_name)
            except (OSError, error): Gui.popup.set_content("Error: can't write in directory '"+file_path+"'", disabled=True, color=Gui.theme.get("link", "hover", "color"))
            Gui.app.init(Gui.popup)

        #print(Gui.app.style.background)
        Gui.app.event(e)
      Gui.app.update()

      screen.flip()
      Vars.clock.tick(60)

  def event_fire(self, method, *arg, **kwargs):
    try: 
      self.verify(method, *arg, **kwargs)
      return method(*arg, **kwargs), None
    except (Exception, BaseException) as e: 
      return None, Exception.with_traceback(KeyboardInterrupt(type(e).__name__+": "+e.args[0]) if type(e) == RuntimeError else e, e.__traceback__.tb_next if DEBUG else None)
