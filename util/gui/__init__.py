"""Modules for creating a widget-based user interface. See the examples folder
for sample scripts that use this module."""
# Module is a part of PGU library, get on https://github.com/parogers/pgu
# I modified the library for emulator use (and because is little bugy XD)

import pygame

# The basestring class was removed in Python 3, but we want to keep it to maintain
# compatibility with previous versions of python.
try:
    __builtins__["basestring"]
except KeyError:
    __builtins__["basestring"] = str

from .errors import *

from .theme import Theme
from .style import Style
from .widget import Widget
from .surface import subsurface, ProxySurface
from .const import *

from .container import Container
from .app import App, Desktop
from . import pguglobals as globalapp
from .table import Table

from .group import Group
from .form import Form

from .basic import Spacer, Label, parse_color, is_color
from .button import Icon, Button, Switch, Link

from .menus import Menu
from .dialog import Dialog
