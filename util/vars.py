from pygame.time import Clock, get_ticks
from webbrowser import open as open_link, register_standard_browsers, register_X_browsers  # To open links in help dropdown
register_standard_browsers()
register_X_browsers()
del register_standard_browsers, register_X_browsers # cleanup namespace
# internal library
from . import gui

"""
benchmarks:
 - epsilon:
   - set_pixel: 130 µs
   - 100*100: fill_rect: 750 µs
   - 1*1: fill_rect: 130 µs
   - draw_string: 640 µs
   - get_pixel: 77 µs
   - color: 180 µs

 - omega:
   - set_pixel: 63 µs
   - 100*100: fill_rect: 740 µs
   - 1*1: fill_rect: 67 µs
   - draw_string: 443 µs
   - get_pixel: 60 µs
   - color: 168 µs

 - upsilon:
   - set_pixel: 80 µs
   - 100*100: fill_rect: 753 µs
   - 1*1: fill_rect: 109 µs
   - draw_string: 426 µs
   - get_pixel: 76 µs
   - color: 210 µs

magic draw ratio (first draw):
  - epsilon: 02:17.713
  - omega: 02:07.797
  - upsilon: 02:22.141
"""

__all__ = [
  "Vars",
  "Colors",
  "Gui",
  "Fonts",
  "Errors"
]

class Colors: 
  red =     (248, 0,   0)
  cyan =    (0,   252, 248)
  blue =    (0,   0,   248)
  grey =    (160, 164, 160)
  green =   (80,  192, 0)
  gray =    (160, 164, 160)
  pink =    (248, 168, 176)
  purple =  (104, 44,  120)
  magenta = (248, 4,   136)
  black =   (0,   0,   0)
  orange =  (248, 132, 24)
  brown =   (136, 112, 80)
  white =   (248, 252, 248)
  yellow =  (248, 252, 0)

  def get(rgbOrName) -> list((int, int, int)):
    if type(rgbOrName) == str: 
      if hasattr(Colors, rgbOrName): return getattr(Colors, rgbOrName)

      elif rgbOrName.startswith('#'):
        if len(rgbOrName) != 7: raise ValueError("RGB hex values are 6 bytes long")
        return [int(rgbOrName[i:i+2], 16) for i in range(1, len(rgbOrName), 2)]

    elif type(rgbOrName) == tuple or type(rgbOrName) == list:
      if len(rgbOrName) != 3: raise TypeError("Color needs 3 components")
      return [int(color) if type(color) == float else color if Errors.type_test(int, color) else "else can't happening XD" for color in rgbOrName]

    raise ValueError("invalid syntax for number")

  def __init__(self, *args): 
    pass

  # color test
  def __eq__(self, object):
    print("==========================", object, type(object))
    if object == int: raise TypeError("Int are not colors")
    elif object == str or object == tuple or object == list: return True
    return False
    
  def __ne__(self, object):
    return not self.__eq__(object)    

class Errors:
  ERRORS = {
    int:   "can't convert {} to float",
    Colors: "object '{}' isn't a tuple or list",
    str:   "can't convert '{}' object to str implicitly"
  } 

  def type_test(_type, *fields):
    if _type not in Errors.ERRORS: raise RuntimeError("invalid test type mode")
    for i in fields:
      if type(i) != _type: raise TypeError(Errors.ERRORS[_type].format(type(i).__name__))
    return True


class Fonts:
  def __init__(self):
    if not Gui._loaded: raise RuntimeError("load Gui first")
    Fonts.small = Gui.app.theme.get("app", '', "small_font")
    Fonts.large = Gui.app.theme.get("app", '', "large_font")


class Gui:
  # Custom class for screenshot popup
  class Popup(gui.Table):
    _sub_save = None
    _area = None
    _hidden = True
    _time_is = 0

    def __init__(self, title, max_size, time_left_ms, **params):
      super(Gui.Popup, self).__init__(**params)

      self._max_letters = max_size
      self._time_left = time_left_ms

      # Create popup
      content = gui.Table()
      self._value = gui.Dialog(title, content, **params)

      content.add(gui.Link("{save_dir}", cls=self._value.cls+".link"))
      content.tr()
      content.add(gui.Label("Will close after "+(str(self._time_left/1000)+" s" if self._time_left > 1000 else str(self._time_left)+" ms"), align=1, disabled=True))

      self.add(self._value, 0, 0) # Add into table to avoid popup from taking up the entire screen
      self.connect(gui.CLICK, self.close)

    def connect(self, code, func, *params):
      self._value.clos.connect(code, func, *params)

    def disconnect(self, code, func=None):
      self._value.clos.disconnect(code, func)

    def set_content(self, text, click_text=None, **params):
      new = gui.Table()

      for i in range(0, len(text), self._max_letters):
        w = gui.Link(text[i:i+self._max_letters], cls=self._value.cls+".link", **params)
        if click_text: w.connect(gui.CLICK, open_link, click_text)
        new.add(w)
        new.tr()
      new.add(gui.Label("Will close after "+(str(int(self._time_left/1000))+"s" if self._time_left > 1000 else str(self._time_left)+"ms"), align=1, disabled=True))

      self._value.set_main(new)

    def close(self):
      self._hidden = True
      self.repaint()

    def is_hidden(self):
      return self._hidden

    def event(self, e):
      gui.Table.event(self, e)
      
      if e.type == gui.ENTER: 
        self._time_is = get_ticks()
        self._hidden = False
        self._sub_save = gui.globalapp.app.screen.copy()
        print(self._sub_save, self._sub_save.get_rect())

    def update(self, s):
      if self._time_is and get_ticks()-self._time_is>self._time_left: 
        self._time_is = 0
        self._value.clos.send(gui.CLICK)
      
      elif self._hidden:
        print(s, self._sub_save.get_rect())
        s.blit(self._sub_save.copy(), (0, 0))

      return gui.Table.update(self, s)


  _loaded = False
  screen_save = None

  def __init__(self, path, start_os, start_model):
    Gui.app = gui.App(theme=gui.Theme(path+"theme"))
    Gui.menu = gui.Table(x=0, y=0, decorate=False)
    #Gui.menu.connect(gui.BLUR, Gui.parse_screen)
    def quit_menu():
      Gui.parse_screen()

      Gui.state.paused = False
    

    # Help dropdown
    new = gui.Menu(Gui.menu, "Help", name="help")
    new.add("CTRL+O: change OS",       disabled=True)
    new.add("CTRL+M: change Model",    disabled=True)
    new.add("CTRL+P: pause/resume",    disabled=True)
    new.add("CTRL+S: take screenshot", disabled=True)
    new.add(gui.Link("GitHub project",),           None, open_link, ("https://github.com/ZetaMap/Kandinsky-Numworks",))
    new.add(gui.Link("Open an Issue",),            None, open_link, ("https://github.com/ZetaMap/Kandinsky-Numworks/issues/new",))
    new.add(gui.Link("Made by ZetaMap", align=1),  None, open_link, ("https://github.com/ZetaMap",))
    self.menu.add(new)

    # OS modes dropdown
    self.create_menu([
      {"name": "PC",       "color": "#4a4a4a", "unit": "deg",     "ratio": 0,   "clock": False},
      {"name": "Numworks", "color": "#ffb531", "unit": "deg",     "ratio": 1,   "clock": False},
      {"name": "Omega",    "color": "#c53431", "unit": "sys/deg", "ratio": 0.8, "clock": True },
      {"name": "Upsilon",  "color": "#7ea2ce", "unit": "sys/deg", "ratio": 0.9, "clock": True },
    ], start_os, "Change OS", "mode")

    # Models dropdown
    self.create_menu([
      {"name": "n0100 unfinish", "ratio": 0, "icon": False, "disabled": True},
      {"name": "n0110",          "ratio": 1, "icon": False                  },
      {"name": "n0120 unfinish", "ratio": 0, "icon": False, "disabled": True},
    ], start_model, "Change Model", "model")

    # State button
    def update(states):
      Gui.update("state", {"paused": not Gui.state.paused})
      Gui.menu.find("state").value = states[Gui.state.paused]   

    w = gui.Button(" Pause", "pause", name="state", focusable=False)
    w.connect(gui.CLICK, update, [gui.Button(" Pause ", "pause").value, gui.Button(" Resume", "resume").value])
    self.menu.add(w)
    Gui.update("state", {"paused": True, "already_paused": False}) # Pause events to give the time of thread to initialize

    # Special button for screenshot popup
    Gui.popup = Gui.Popup("Screenshot saved at", 40, 5000, name="popup")
    def hide():
      Gui.app.init(Gui.menu)
      if Gui.state.already_paused: Gui.state.already_paused = False
      else: Gui.state.paused = False
    Gui.popup.connect(gui.CLICK, hide)
  
    # Load finished
    Gui.height = self.menu.resize()[1]
    Gui._loaded = True
    
  def create_menu(self, options, start_default, label, name):
    group = gui.Group(name, options[start_default[0] if 0 <= start_default[0] <= len(options) else start_default[1]])
    new = gui.Menu(Gui.menu, label, name=group.name+"-menu", focusable=False)

    for mode in options: 
      w = new.add(' '*bool(mode.get("icon", True))+mode["name"], mode["name"].lower() if mode.get("icon", True) else None, Gui.update, (group.name, mode), disabled=mode.get("disabled", False))
      if mode == group.value: w.send(gui.CLICK)
    
    self.menu.add(group)
    self.menu.add(new)

  def update(field, content):
    setattr(Gui, field, getattr(Gui, field)(**content) if hasattr(Gui, field) else content if isinstance(content, StateData) else StateData(**content))
    w = Gui.menu.find(field)
    if w and isinstance(w, gui.Group): w.value = content

  def move_focus(menu, focus=None):
    w = Gui.menu.find(menu)
    if w:
      if hasattr(w, "widgets"):
        print(w.widgets._next(w.widgets.myfocus) or w.widgets._next(), w.widgets.myfocus.connects[32851][0].params)
        w = w.widgets.myfocus

      w.send(gui.CLICK)

  def is_loaded():
    if not Gui._loaded: raise RuntimeError("load Gui first")

  def save_screen(): 
    Gui.is_loaded()
    if Gui.screen_save == None:
      Gui.state.paused = True
      Gui.screen_save = Gui.app.screen.subsurface((0, Gui.height, Vars.screen[0], Vars.screen[1]-Gui.height))

  def parse_screen(): 
    Gui.is_loaded()
    if Gui.screen_save:
      Gui.screen_save.set_clip(gui.pygame.Rect(10, 10, 100, 100))
      Gui.app.screen.blit(Gui.screen_save.copy(), (0, Gui.height))
            

# Data class for buttons
class StateData:
  __field_name__ = ""

  def __init__(self, **content):
    self(**content)

  def __call__(self, **content):
    for k, v in content.items(): setattr(self, k, v)
    return self

  def __str__(self):
    return "<{} ({})>".format(__class__.__name__, self.__dict__)

  def __repr__(self):
    return self.__str__()

  def has(self, name):
    return hasattr(self, name)

  def get(self, name, default=None):
    return getattr(self, name, default)


class Vars:
  dirchar = '/' if __file__[0] == '/' else '\\'
  poop=__module__.split('.')[0]
  path = __file__[:__file__.rindex(poop)+len(poop)]+dirchar+"util"+dirchar
  del poop
  app_name = "Kandinsky Emulator"
  app_icon = None
  top_size = None
  header_size = 19
  screen = (320, 222+header_size) # default size, without menus
  clock = Clock()

  def __init__(self):
    if not Gui._loaded: raise RuntimeError("load Gui first")
    Vars.app_icon = Gui.app.theme.get("app", '', "icon")
    Vars.top_size = Gui.height+self.header_size
    Vars.screen = (320, 222+self.top_size)