from .tests import Tests
from .vars import Vars

class Colors:
  """https://github.com/numworks/epsilon/blob/master/kandinsky/include/kandinsky/color.h"""

  blue    = (0,   0,   248)
  b       = blue
  red     = (248, 0,   0)
  r       = red
  green   = (80,  192, 0)
  g       = green
  yellow  = (248, 252, 0)
  y       = yellow
  brown   = (136, 112, 80)
  black   = (0,   0,   0)
  k       = black
  white   = (248, 252, 248)
  w       = white
  pink    = (248, 168, 176)
  orange  = (248, 132, 24)
  purple  = (104, 44,  120)
  grey    = (160, 164, 160)
  gray    = grey
  cyan    = (0,   252, 248)
  magenta = (248, 4,   136)
  COLORS = {k: v for k, v in locals().items() if not k.startswith('_')}

  fix = lambda r, g, b, expand=Vars.selected_os <= 1: (
    (Colors.expand((r>>3)&0x1f, 5) if expand else ((r>>3)&0x1f)<<3),
    (Colors.expand((g>>2)&0x3f, 6) if expand else ((g>>2)&0x3f)<<2),
    (Colors.expand((b>>3)&0x1f, 5) if expand else ((b>>3)&0x1f)<<3))
  fix2 = lambda *values, expand=Vars.selected_os <= 1: (
    tuple(Colors.expand(Colors.contract(c, i%2, 3), 5+i%2) for i, c in enumerate(*values)) 
      if expand else
    tuple(Colors.contract(c, i%2, 3)<<(3-i%2) for i, c in enumerate(*values)))
  contract = lambda v, nBits, length=8: (v>>(length-nBits))&(2**(4+length-nBits)-1)
  expand = lambda v, nBits, length=8: (v<<(length-nBits))|(v>>(nBits-(length-nBits)))

  def convert(rgbOrName):
    _type = type(rgbOrName)

    if _type == str:
      if rgbOrName in Colors.COLORS: return Colors.fix(*Colors.COLORS[rgbOrName], Vars.selected_os <= 1)
      elif rgbOrName.startswith('#'):
        if len(rgbOrName) != 7: raise ValueError("RGB hex values are 6 bytes long")

        try: return Colors.fix(*[int(rgbOrName[i:i+2], 16) for i in range(1, len(rgbOrName), 2)], Vars.selected_os <= 1)
        except ValueError as e:
          e.args = (f"invalid literal for int() with base 16: '{rgbOrName[1:]}'",)
          raise
      else:
        try: ratio = float(rgbOrName)
        except ValueError as e:
          e.args = ("invalid syntax for number",)
          raise
        else:
          if 0 <= ratio <= 1: return tuple([int(255*ratio) for _ in range(3)])
          else: raise ValueError("Gray levels are between 0.0 and 1.0")

    elif _type == int: raise ValueError("Int are not colors")

    Tests.list(rgbOrName)
    if len(rgbOrName) != 3: raise ValueError("Color needs 3 components")
    return Colors.fix(*[int(c) for c in rgbOrName if type(c) == float or Tests.int(c)], Vars.selected_os <= 1)
