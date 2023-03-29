from sdl2.keyboard import SDL_GetKeyboardState, SDL_GetScancodeFromKey
from sdl2.ext.common import get_events
from sdl2.events import SDL_KEYDOWN
from sdl2.keycode import *
from random import randint, random

__all__ = ["Ion"]

class IonKey:
  def __init__(self, name, code_or_codes, ion_code, display_name=None, computer_equivalent=None, name_filler="KEY_"):
    self.name = name_filler+name
    if type(code_or_codes) in (tuple, list):
      assert len(code_or_codes), "list of codes must have minimum 1 code"
      self.codes = tuple(code_or_codes)
    else: self.codes = (code_or_codes,)
    self.ion_code = ion_code
    self.display_name = display_name if display_name else name.lower()
    self.computer_name = computer_equivalent if computer_equivalent else self.display_name.title()

  def is_pressed(self, event):
    for i in self.codes:
      if event.key.keysym.sym == i: return True
    return False


class Ion:
  """Ion integration of numworks
  Why in this library? because sdl2 is used here, and ion-numworks module will use this class if this library is present
  """

  KEYS = [
    IonKey("LEFT",  SDLK_LEFT,   0),
    IonKey("RIGHT", SDLK_RIGHT,  1),
    IonKey("DOWN",  SDLK_DOWN,   2),
    IonKey("UP",    SDLK_UP,     3),
    IonKey("OK",    SDLK_INSERT, 4, "OK",    "Insert"),
    IonKey("BACK",  SDLK_DELETE, 5, None,    "Delete"),
    IonKey("HOME",  SDLK_ESCAPE, 6, None,    "Escape"),
    IonKey("ONOFF", SDLK_END,    7, "onOff", "End"),
    IonKey("SHIFT", (SDLK_LSHIFT, SDLK_RSHIFT), 12),
    IonKey("ALPHA", (SDLK_LCTRL, SDLK_RCTRL),   13, None, "CTRL"),
    IonKey("XNT",   SDLK_x,      14, None, 'X'),
    IonKey("VAR",   SDLK_v,      15, None, 'V'),
    IonKey("TOOLBOX",   SDLK_QUOTEDBL, 16, None, '"'),
    IonKey("BACKSPACE", (SDLK_BACKSPACE, SDLK_KP_BACKSPACE), 17),
    IonKey("EXP",   SDLK_e,      18, None, 'E'),
    IonKey("LN",    SDLK_n,      19, None, 'N'),
    IonKey("LOG",   SDLK_l,      20, None, 'L'),
    IonKey("IMAGINARY", SDLK_i,  21, None, 'I'),
    IonKey("COMMA",   (SDLK_COMMA, SDLK_KP_COMMA), 22, None, ','),
    IonKey("POWER",   (SDLK_CARET, SDLK_KP_POWER), 23, None, '^'),
    IonKey("SINE",    SDLK_s, 24, "sin", 'S'),
    IonKey("COSINE",  SDLK_c, 25, "cos", 'C'),
    IonKey("TANGENT", SDLK_t, 26, "tan", 'T'),
    IonKey("PI",      SDLK_p, 27, None,  'P'),
    IonKey("SQRT",    SDLK_r, 28, None,  'R'),
    IonKey("SQUARE",  (SDLK_GREATER, SDLK_KP_GREATER), 29, None, ">"),
    IonKey("SEVEN",   (SDLK_7, SDLK_KP_7), 30, '7'),
    IonKey("EIGHT",   (SDLK_8, SDLK_KP_8), 31, '8'),
    IonKey("NINE",    (SDLK_9, SDLK_KP_9), 32, '9'),
    IonKey("LEFTPARENTHESIS",  (SDLK_LEFTPAREN, SDLK_KP_LEFTPAREN),   33, '('),
    IonKey("RIGHTPARENTHESIS", (SDLK_RIGHTPAREN, SDLK_KP_RIGHTPAREN), 34, ')'),
    IonKey("FOUR",  (SDLK_4, SDLK_KP_4),   36, '4'),
    IonKey("FIVE",  (SDLK_5, SDLK_KP_5),   37, '5'),
    IonKey("SIX",   (SDLK_6, SDLK_KP_6),   38, '6'),
    IonKey("MULTIPLICATION", (SDLK_ASTERISK, SDLK_KP_MULTIPLY), 39, '*'),
    IonKey("DIVISION",       (SDLK_SLASH, SDLK_KP_DIVIDE),      40, '/'),
    IonKey("ONE",   (SDLK_1, SDLK_KP_1),   42, '1'),
    IonKey("TWO",   (SDLK_2, SDLK_KP_2),   43, '2'),
    IonKey("THREE", (SDLK_3, SDLK_KP_3),   44, '3'),
    IonKey("PLUS",  (SDLK_PLUS, SDLK_KP_PLUS),      45, '+'),
    IonKey("MINUS", (SDLK_MINUS, SDLK_KP_MINUS),    46, '-'),
    IonKey("ZERO",  (SDLK_0, SDLK_KP_0),            48, '0'),
    IonKey("DOT",   (SDLK_PERIOD, SDLK_KP_PERIOD),  49, '.'),
    IonKey("EE",    (SDLK_EXCLAIM, SDLK_KP_EXCLAM), 50, "EE", '!'),
    IonKey("ANS",   SDLK_a,   51, "Ans", 'A'),
    IonKey("EXE" ,  (SDLK_RETURN, SDLK_KP_ENTER),   52, "EXE", "Return"),
  ]
  brightness = 240
  
  def _apply_keys_to_module(module):
    module.__dict__.update({k.name: k.ion_code for k in Ion.KEYS})

  def get_keys():
    pressed = set()

    for e in get_events():
      if e.type == SDL_KEYDOWN: 
        for k in Ion.KEYS:
          if k.is_pressed(e):
            pressed.add(k.display_name)
            break

    return pressed

  def keydown(key):
    # Find the key
    for k in Ion.KEYS:
      if k.ion_code == key: 
        key = k
        break
    else: return False

    return any([e.type == SDL_KEYDOWN and key.is_pressed(e) for e in get_events()])

  def battery():
    return 4.20+randint(900, 1500)/10**5+random()/10**5

  def battery_level():
    return 3

  def battery_ischarging():
    return False

  def set_brightness(level):
    level %= 256
    Ion.brightness = 240 if level > 240 else level

  def get_brightness():
    return Ion.brightness



#import sys
#import termios
#import tty
#
#def getchr():
#    r"""
#    Get a single key from the terminal without printing it.
#    Certain special keys return several "characters", all starting with the
#    escape character '\x1b'. You could react to that by reading two more
#    characters, but the actual escape key will only make this return a single
#    escape character, and since it's blocking, that wouldn't be a good solution
#    either.
#    """
#    fd = sys.stdin.fileno()
#    old = termios.tcgetattr(fd)
#    tty.setraw(sys.stdin.fileno())
#    ch = sys.stdin.read(1)
#    termios.tcsetattr(fd, termios.TCSADRAIN, old)
#    if ord(ch) == 3:  # ^C
#        raise KeyboardInterrupt
#    return ch
