from sdl2 import SDL_Rect, SDL_FillRect, SDL_BlitSurface, SDL_BlitScaled, SDL_CreateRGBSurfaceWithFormat, SDL_PIXELFORMAT_RGB888
from sdl2.ext import prepare_color
from ctypes import cast, byref, POINTER, c_uint, c_uint8
from .vars import Vars

__all__ = ["Draw"]


class Draw:
  new_area = lambda *area: SDL_Rect(*[int(i*Vars.zoom_ratio) for i in (area[0] if len(area)==1 and type(area[0]) in (list, tuple) else area)])
  new_surface = lambda width, height: SDL_CreateRGBSurfaceWithFormat(0, int(width*Vars.zoom_ratio), int(height*Vars.zoom_ratio), 32, SDL_PIXELFORMAT_RGB888).contents
  blit = lambda dest, source, area=None: SDL_BlitSurface(source, None, dest, Draw.new_area(area) if area else None)
  blit_scaled = lambda dest, source, area=None: SDL_BlitScaled(source, None, dest, Draw.new_area(area+(source.w, source.h) if len(area) == 2 else area) if area else None)
  rect = lambda dest, color, area=None: SDL_FillRect(dest, Draw.new_area(area) if area else None, prepare_color(color, dest))
  pixel = lambda dest, color, x, y: SDL_FillRect(dest, Draw.new_area(x, y, 1, 1), prepare_color(color, dest))
  string = lambda dest, font, text, x, y, color=None: Draw.blit_scaled(dest, font.render(text, color=color), (x, y))

  def get_at(source, x, y):
    pixel = cast(byref(cast(source.pixels, POINTER(c_uint8)).contents, (source.w*y+x)*source.format.contents.BytesPerPixel), POINTER(c_uint)).contents.value
    return (pixel&0xff0000)>>8, (pixel&0x00ff00)>>4, (pixel&0x0000ff)>>0
