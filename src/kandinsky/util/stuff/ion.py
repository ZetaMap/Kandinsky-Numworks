from sdl2.keyboard import SDL_GetKeyboardState, SDL_GetKeyboardFocus
from sdl2.keycode import *
from random import randint, random

__all__ = ["Ion"]
SDLK_ = None # temporaly, TODO: find keys for specials numworks keys


class KeyData:
  def __init__(self, name, code, ion_code=None, display_name=None, filler="KEY_"):
    self.name = filler+name
    self.codes = [code]
    self.ion_code = ion_code if ion_code else code
    self.display_name = display_name if display_name else name.lower()

  def add_code(self, new_code):
    self.codes.append(new_code)
    return self

  def test_code(self, code):
    return SDL_GetKeyboardFocus() and SDL_GetKeyboardState(code)

  def is_pressed(self, code=None):
    if code is None: return all([1 for i in self.codes if self.test_code(i)])
    elif code < 0 or code > len(self.codes): return False
    else: return self.test_code(self.codes[code])

class Ion:
  """Ion integration of numworks
  Why here? because sdl2 is defined here, and ion-numworks module will use this if present
  """

  KEYS = [
    KeyData("LEFT",  SDLK_LEFT,  0),
    KeyData("RIGHT", SDLK_RIGHT, 1),
    KeyData("DOWN",  SDLK_DOWN,  2),
    KeyData("UP",    SDLK_UP,    3),
    KeyData("OK",    SDLK_, 4, "OK"),
    KeyData("BACK",  SDLK_, 5),
    KeyData("HOME",  SDLK_, 6),
    KeyData("ONOFF", SDLK_, 7, "onOff"),
    KeyData("SHIFT", SDLK_LSHIFT, 12).add_code(SDLK_RSHIFT),
    KeyData("ALPHA", SDLK_LCTRL,  13).add_code(SDLK_RCTRL),
    KeyData("XNT",   SDLK_x, 14),
    KeyData("VAR",   SDLK_, 15),
    KeyData("TOOLBOX",   SDLK_, 16),
    KeyData("BACKSPACE", SDLK_DELETE, 17),
    KeyData("EXP", SDLK_, 18),
    KeyData("LN",  SDLK_, 19),
    KeyData("LOG", SDLK_, 20),
    KeyData("IMAGINARY", SDLK_i, 21),
    KeyData("COMMA",   SDLK_COMMA, 22),
    KeyData("POWER",   SDLK_CARET, 23).add_code(SDLK_KP_POWER),
    KeyData("SINE",    SDLK_s, 24, "sin"),
    KeyData("COSINE",  SDLK_c, 25, "cos"),
    KeyData("TANGENT", SDLK_t, 26, "tan"),
    KeyData("PI",      SDLK_p, 27),
    KeyData("SQRT",    SDLK_, 28),
    KeyData("SQUARE",  SDLK_SYSREQ, 29),
    KeyData("SEVEN",   SDLK_7, 30, '7').add_code(SDLK_KP_7),
    KeyData("EIGHT",   SDLK_8, 31, '8').add_code(SDLK_KP_8),
    KeyData("NINE",    SDLK_9, 32, '9').add_code(SDLK_KP_9),
    KeyData("LEFTPARENTHESIS",  SDLK_LEFTPAREN,  33, '('),
    KeyData("RIGHTPARENTHESIS", SDLK_RIGHTPAREN, 34, ')'),
    KeyData("FOUR", SDLK_4, 36, '4').add_code(SDLK_KP_4),
    KeyData("FIVE", SDLK_5, 37, '5').add_code(SDLK_KP_5),
    KeyData("SIX",  SDLK_6, 38, '6').add_code(SDLK_KP_6),
    KeyData("MULTIPLICATION", SDLK_ASTERISK, 39, '*').add_code(SDLK_KP_MULTIPLY),
    KeyData("DIVISION",       SDLK_SLASH,    40, '/').add_code(SDLK_KP_DIVIDE),
    KeyData("ONE",   SDLK_1,      42, '1').add_code(SDLK_KP_1),
    KeyData("TWO",   SDLK_2,      43, '2').add_code(SDLK_KP_2),
    KeyData("THREE", SDLK_3,      44, '3').add_code(SDLK_KP_3),
    KeyData("PLUS",  SDLK_PLUS,   45, '+').add_code(SDLK_KP_PLUS),
    KeyData("MINUS", SDLK_MINUS,  46, '-').add_code(SDLK_KP_MINUS),
    KeyData("ZERO",  SDLK_0,      48, '0').add_code(SDLK_KP_0),
    KeyData("DOT",   SDLK_PERIOD, 49, '.').add_code(SDLK_KP_PERIOD),
    KeyData("EE",    SDLK_, 50, "EE"),
    KeyData("ANS",   SDLK_, 51, "Ans"),
    KeyData("EXE" ,  SDLK_RETURN, 52, "EXE").add_code(SDLK_KP_ENTER)
  ]
  brightness = 240
  
  def get_keys():
    return set([key.display_name for key in Ion.KEYS if key.is_pressed()])

  def keydown(key):
    for i in Ion.KEYS:
      if i.ion_code == key: return i.is_pressed()
    return False

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

"""Some keyboard keys found

https://github.com/Tatone26/Numworks-python-games/
KEY_EXE = "space"
KEY_UP = "up"
KEY_DOWN = "down"
KEY_RIGHT = "right"
KEY_LEFT = "left"
KEY_OK = "return"
KEY_BACK = "delete"
KEY_HOME = "windows"
KEY_ONOFF = "echap"
KEY_SHIFT = "shift"
KEY_ALPHA = "ctrl"
KEY_XNT = "n"
KEY_VAR = "F1"
KEY_TOOLBOX = "F2"
KEY_EXP = "e"
KEY_LN = "z"
KEY_LOG = "l"
KEY_IMAGINARY = "i"
KEY_COMMA = ","
KEY_POWER = "^"
KEY_SINE = "s"
KEY_COSINE = "c"
KEY_TANGENT = "t"
KEY_PI = "p"
KEY_SQRT = "_"
KEY_SQUARE = "²"
KEY_EIGHT = "eight"
KEY_SEVEN = "seven"
KEY_NINE = "nine"
KEY_ONE = "one"
KEY_TWO = "two"
KEY_THREE = "three"
KEY_RIGHTPARENTHESIS = ")"
KEY_LEFTPARENTHESIS = "("
KEY_FOUR = "four"
KEY_FIVE = "five"
KEY_SIX = "six"
KEY_MULTIPLICATION = "multiplication"
KEY_DIVISION = "division"
KEY_MINUS = "minus"
KEY_PLUS = "plus"
KEY_ZERO = "zero"
KEY_DOT = "dot"
KEY_EE = "!"
KEY_ANS = "a"

"""