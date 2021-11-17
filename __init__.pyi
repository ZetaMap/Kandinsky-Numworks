from typing import Tuple, List, NoReturn, Union, Optional

_ColorInput = Union[Tuple[int, int, int], List[int, int, int], str]
_ColorOutput = Tuple[int, int, int]

def get_pixel(x: int, y: int) -> _ColorOutput: pass
def set_pixel(x: int, y: int, color: _ColorInput) -> None: pass
def color(r: int, g: int, b: int) -> _ColorOutput: pass
def draw_string(
  text: str, 
  x: int, 
  y: int, 
  color: Optional[_ColorInput]=(), 
  background: Optional[_ColorInput]=()) -> None: pass
def fill_rect(x: int, y: int, width: int, height: int, color: _ColorInput) -> None: pass
def display() -> NoReturn | None: pass
