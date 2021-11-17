from typing import NoReturn, List, Tuple, Literal, Union

_ColorInput = Union[Tuple[int, int, int], List[int, int, int], str]
_ColorOutput = Tuple[int, int, int]

class KS:
  def __init__() -> None: pass
  def draw_content() -> None: pass
  
  def get_pixel(x: int, y: int) -> _ColorOutput: pass
  def set_pixel(x: int, y: int, color: _ColorInput) -> None: pass
  def color(r: int, g: int, b: int) -> _ColorOutput: pass
  def drawString(
    text: str, 
    x: int, 
    y: int, 
    color: _ColorInput, 
    background: _ColorInput) -> None: pass
  def draw_string(
    text: str,
    x: int, 
    y: int, 
    color: _ColorInput, 
    background: _ColorInput) -> None: pass
  def fill_rect(x: int, y: int, width: int, height: int, color: _ColorInput) -> None: pass
  def display() -> NoReturn: pass
  
  def refresh(withError: bool=True) -> None: pass
  def convert_color(color: _ColorInput) -> _ColorOutput: pass
  def type_test(
    _object: Union[int, _ColorInput],
    mode: Literal["int", "color", "str"]="int") -> None: pass