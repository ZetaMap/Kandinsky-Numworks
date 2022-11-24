from sdl2 import SDL_Rect, SDL_FillRect, SDL_BlitSurface, SDL_CreateRGBSurfaceWithFormat, SDL_PIXELFORMAT_ARGB8888, Uint8
from sdl2.ext import prepare_color
from ctypes import cast, byref, POINTER, c_uint

__all__ = ["Draw"]


class Draw:
  new_surface = lambda width, height: SDL_CreateRGBSurfaceWithFormat(0, width, height, 32, SDL_PIXELFORMAT_ARGB8888)
  blit = lambda dest, source, area=None: SDL_BlitSurface(source, None, dest, SDL_Rect(*area) if area else None)
  rect = lambda dest, color, area=None: SDL_FillRect(dest, SDL_Rect(*area) if area else None, prepare_color(color, dest))
  pixel = lambda dest, color, x, y: SDL_FillRect(dest, SDL_Rect(x, y, 1, 1), prepare_color(color, dest))

  def get_at(source, x, y):
    bpp = source.format.contents.BytesPerPixel
    pixel = hex(cast(byref(cast(source.pixels, POINTER(Uint8)).contents, bpp*source.w*y+x*bpp), POINTER(c_uint)).contents.value)
    return int(pixel[2:4], 16), int(pixel[4:6], 16),int(pixel[6:8], 16)
