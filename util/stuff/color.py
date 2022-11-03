COLOR_ROUND_MULTIPLIER = (8, 4, 8)

class Colors:
  red     = (248, 0,   0)
  cyan    = (0,   252, 248)
  blue    = (0,   0,   248)
  grey    = (160, 164, 160)
  gray    = grey
  green   = (80,  192, 0)
  pink    = (248, 168, 176)
  purple  = (104, 44,  120)
  magenta = (248, 4,   136)
  black   = (0,   0,   0)
  orange  = (248, 132, 24)
  brown   = (136, 112, 80)
  white   = (248, 252, 248)
  yellow  = (248, 252, 0)

  def convert(rgbOrName):
    color = []
    _type = type(rgbOrName)

    if _type == str: 
      if rgbOrName.startswith("__"): pass
      elif hasattr(Colors, rgbOrName): color = getattr(Colors, rgbOrName)
      elif rgbOrName.startswith('#'):
        if len(rgbOrName) != 7: raise ValueError("RGB hex values are 6 bytes long")

        try: color = [int(rgbOrName[i:i+2], 16) for i in range(1, len(rgbOrName), 2)]
        except ValueError as e:
          e.args = (f"invalid literal for int() with base 16: '{rgbOrName[1:]}'",)
          raise

    elif _type == tuple or _type == list:
      if len(rgbOrName) != 3: raise ValueError("Color needs 3 components")
      for c in rgbOrName:
        _type = type(c)
        if _type != float and _type != int: raise TypeError(f"can't convert {_type.__name__} to int")

        color.append(int(c))

    elif _type == int: raise ValueError("Int are not colors")
    else: raise TypeError(f"object '{_type.__name__}' isn't a tuple or list")

    if len(color) > 0: return tuple([0 if color[i] < 0 else color[i]%256//COLOR_ROUND_MULTIPLIER[i]*COLOR_ROUND_MULTIPLIER[i] for i in range(len(color))])
    else: raise ValueError("invalid syntax for number")
