from typing import Tuple, List, Union, Optional

_ColorInput = Union[Tuple[int, int, int], List[int, int, int], str]
_ColorOutput = Tuple[int, int, int]

def get_pixel(x: int, y: int) -> _ColorOutput: pass
def set_pixel(x: int, y: int, color: _ColorInput) -> None: pass
def color(color: _ColorInput) -> _ColorOutput: pass
def color(r: int, g: int, b: int) -> _ColorOutput: pass
def draw_string(text: str, x: int, y: int, color: Optional[_ColorInput]=(0, 0, 0), background: Optional[_ColorInput]=(248, 252, 248)) -> None: pass
def fill_rect(x: int, y: int, width: int, height: int, color: _ColorInput) -> None: pass

# Special method, only in pc
def quit() -> None: pass