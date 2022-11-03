from sdl2 import SDL_RWFromFile, SDL_SaveBMP_RW
from sdl2.sdlimage import IMG_SavePNG_RW, IMG_Load, IMG_SaveJPG_RW
from sdl2.ext.ttf import FontManager

from configparser import ConfigParser
import os

__all__ = [
  "Constants",
  "Config",
  "StateData"
]

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

class Constants:
  base_name=__module__.split('.')[1]
  path = __file__[:__file__.rindex(base_name)+len(base_name)+1]+"data/"
  # Test if path correct
  if not os.path.exists(path): path = __file__[:__file__.rindex(base_name)]+"data/"

  app_name = "Kandinsky Emulator"
  app_icon = None
  head_size = 18
  screen = (320, 222)

  image_formats = [("PNG", ".png"), ("Bitmap", ".bmp"), ("All files", ".*")]
  if os.name != "posix": image_formats.insert(1, ("JPEG", (".jpg", ".jpeg")))


class Config:
  open = lambda path, mode='w': SDL_RWFromFile(path.encode("utf-8"), bytes(mode, "utf-8"))
  save_image = lambda surface, path: (SDL_SaveBMP_RW(surface, Config.open(path), 1) if path.endswith(".bmp") else 
                                      IMG_SaveJPG_RW(surface, Config.open(path), 1, 80) if os.name != "posix" and path.endswith((".jpg", ".jpeg")) else
                                      IMG_SavePNG_RW(surface, Config.open(path), 1))

  font = FontManager(Constants.path+"font.ttf", 16)

  os_list = (
    {"name": "PC",       "ratio": 0,   "color": "#4a4a4a", "head": "head1.png"},
    {"name": "Numworks", "ratio": 1,   "color": "#ffb531", "head": "head1.png"},
    {"name": "Omega",    "ratio": 0.8, "color": "#c53431", "head": "head2.png"},
    {"name": "Upsilon",  "ratio": 0.9, "color": "#7ea2ce", "head": "head3.png"},
  )

  model_list = (
    {"name": "n0100", "ratio": 0, "disabled": True },
    {"name": "n0110", "ratio": 1},
    {"name": "n0120", "ratio": 0, "disabled": True },
  )



# Class for some data
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
