from sdl2 import SDL_Rect, SDL_FillRect, SDL_GetRGB, SDL_BlitSurface, SDL_CreateRGBSurfaceWithFormat, SDL_MapRGB, SDL_PIXELFORMAT_ARGB8888, Uint8
from sdl2.ext import prepare_color
from ctypes import cast, POINTER

__all__ = ["Draw"]


class Draw:
  new_surface = lambda width, height: SDL_CreateRGBSurfaceWithFormat(0, width, height, 32, SDL_PIXELFORMAT_ARGB8888)
  blit = lambda dest, source, area=None: SDL_BlitSurface(source, None, dest, SDL_Rect(*area) if area else None)
  rect = lambda dest, color, area=None: SDL_FillRect(dest, SDL_Rect(*area) if area else None, prepare_color(color, dest))
  pixel = lambda dest, color, x, y: SDL_FillRect(dest, SDL_Rect(x, y, 1, 1), prepare_color(color, dest))

  def get_at(source, x, y):
    r, g, b = POINTER(Uint8), POINTER(Uint8), POINTER(Uint8)
    SDL_GetRGB(cast(source.pixels, POINTER(Uint8))+y*source.pitch+x*source.format.BytesPerPixel, source.format, r, g, b)
    return r, b, b
