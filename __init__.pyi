from typing import Tuple, NoReturn

_Color = Tuple[int, int, int]

def get_pixel(x: int, y: int) -> _Color: pass
def set_pixel(x: int, y: int, color: _Color) -> None: pass
def color(r: int, g: int, b: int) -> _Color: pass
def draw_string(text: str, x: int, y: int, color: _Color=(), background: _Color=()) -> None: pass
def fill_rect(x: int, y: int, width: int, height: int, color: _Color) -> None: pass
def display() -> NoReturn: pass
