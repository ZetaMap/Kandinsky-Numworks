"""Contains various types of button widgets."""

from pygame.locals import *

from .const import *
from . import widget, surface
from . import basic, table

class _button(widget.Widget):
    # The underlying 'value' accessed by the getter and setters below
    _value = None

    def __init__(self,**params):
        super(_button, self).__init__(**params)
        self.state = 0

    def event(self,e):
        if e.type == ENTER: self.repaint()
        elif e.type == EXIT: self.repaint()
        elif e.type == FOCUS: self.repaint()
        elif e.type == BLUR: self.repaint()
        elif e.type == KEYDOWN:
            if self.focusable and (e.key == K_SPACE or e.key == K_RETURN):
                self.state = 1
                self.repaint()
        elif e.type == MOUSEBUTTONDOWN:
            self.state = 1
            self.repaint()
        elif e.type == KEYUP:
            if self.state == 1:
                sub = pygame.event.Event(CLICK,{'pos':(0,0),'button':1})
                #self.send(sub.type,sub)
                self._event(sub)
                #self.event(sub)
                #self.click()

            self.state = 0
            self.repaint()
        elif e.type == MOUSEBUTTONUP:
            self.state = 0
            self.repaint()
        elif e.type == CLICK:
            self.click()

        self.pcls = ""
        if self.state == 0 and self.is_hovering():
            self.pcls = "hover"
        if self.state == 1 and self.is_hovering():
            self.pcls = "down"

    def click(self):
        pass


class Button(_button):
    """A button, buttons can be clicked, they are usually used to set up callbacks.

    Example:
        w = gui.Button("Click Me")
        w.connect(gui.CLICK, fnc, value)
        # Assign a new button label
        w.value = "Hello World"

    """

    # The icon of button
    _icon = None

    def __init__(self, value=None, icon=None, **params):
        """Button constructor, which takes either a string label or widget.

        See Widget documentation for additional style parameters.

        """
        params.setdefault('cls', 'button')
        super(Button, self).__init__(**params)
        self._icon = icon
        self.value = value

    @property
    def value(self):
        return self._value

    # Mofidied for personal use
    @value.setter
    def value(self, val):
        if isinstance(val, str):
            # Allow the choice of font to propagate to the button label
            params = {}
            if (self.style.font): params["font"] = self.style.font
            if (self.style.align): params["align"] = self.style.align

            ta = table.Table(**params, disabled=self.disabled)
            if self._icon: ta.add(Icon(self._icon.strip()))
            ta.add(basic.Label(val, cls=self.cls+".label", **params, disabled=self.disabled))
            ta.container = self
            val = ta

        oldval = self._value
        self._value = val

        if (val != oldval):
            # Notify any listeners that we've changed the label
            self.send(CHANGE)
            # Resize as needed
            self.chsize()

    def resize(self,width=None,height=None):
        self.value.rect.x,self.value.rect.y = 0,0
        self.value.rect.w,self.value.rect.h = self.value.resize(width,height)
        return self.value.rect.w,self.value.rect.h

    def paint(self,s):
        rect = self.value.rect
        if (self.pcls == "down"):
            # Shift the contents down to emphasize the button being pressed. This
            # is defined in the theme config file.
            rect = rect.move((self.style.down_offset_x, self.style.down_offset_y))
        self.value.pcls = self.pcls
        self.value.paint(surface.subsurface(s, rect))


# Modified for personal use
class Switch(_button):
    """A switch can have two states, on or off."""

    def __init__(self, w=None,value=False,**params):
        params.setdefault('cls','switch')
        super(Switch, self).__init__(**params)
        self.value = value

        img = self.style.off
        self.style.width = img.get_width()
        self.style.height = img.get_height()

    def paint(self,s):
        #self.pcls = ""
        #if self.container.myhover is self: self.pcls = "hover"
        if self.value: img = self.style.on
        else: img = self.style.off
        s.blit(img,(0,0))

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        oldval = self._value
        self._value = val
        if oldval != val:
            self.send(CHANGE)
            self.repaint()

    def click(self):
        self.value = not self.value


class Icon(_button):
    """TODO - might be deprecated
    """
    def __init__(self,cls,**params):
        params['cls'] = cls
        super(Icon, self).__init__(**params)
        s = self.style.image
        self.style.width = s.get_width()
        self.style.height = s.get_height()
        self.state = 0

    def paint(self,s):
        #self.pcls = ""
        #if self.state == 0 and hasattr(self.container,'myhover') and self.container.myhover is self: self.pcls = "hover"
        #if self.state == 1 and hasattr(self.container,'myhover') and self.container.myhover is self: self.pcls = "down"
        s.blit(self.style.image,(0,0))


class Link(_button):
    """A link, links can be clicked, they are usually used to set up callbacks.
    Basically the same as the button widget, just text only with a different cls.
    Made for convenience.

    Example:
        w = gui.Link("Click Me")
        w.connect(gui.CLICK,fnc,value)

    """
    def __init__(self,value,**params):
        params.setdefault('focusable',True)
        params.setdefault('cls','link')
        super(Link, self).__init__(**params)
        self.value = value
        self.font = self.style.font
        self.style.width, self.style.height = self.font.size(self.value)

    def paint(self,s):
        s.blit(self.font.render(self.value, True, self.style.color),(0,0))
