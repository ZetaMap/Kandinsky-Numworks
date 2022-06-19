from typing import NoReturn, List, Tuple, Union, Literal, Any, Dict

_ColorInput = Union[Tuple[int, int, int], List[int, int, int], str]
_ColorOutput = Tuple[int, int, int]

class Core:
  def __init__() -> None: pass
  def verify(method: str, *args: Any, no_error: bool=False, **kwargs: Dict[str, Any]) -> None: pass
  def sleep(delay_ns: int) -> None: pass
  def get_info(name: str) -> str: pass
  def draw_header() -> None: pass
  
  def get_pixel(x: int, y: int) -> _ColorOutput: pass
  def set_pixel(x: int, y: int, color: _ColorInput) -> None: pass
  def color(rOrList: int, g: int, b: int) -> _ColorOutput: pass
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
  
  def convert_color(color: _ColorInput) -> _ColorOutput: pass
  def type_test(
    _object: Union[int, _ColorInput],
    mode: Literal["int", "color", "str"]="int") -> None: pass
  def event_loop() -> NoReturn: pass
  def event_fire(method: function, *arg: Any, **kwargs: Any) -> List[Any, Union[Exception, None]]: pass
