"""
"""
from .const import *
from . import table, basic, button

class _Menu_Options(table.Table):
    def __init__(self, menu, **params):
        super(_Menu_Options, self).__init__(**params)

        self.menu = menu

    def event(self, e):
        handled = False
        arect = self.get_abs_rect()

        if e.type == MOUSEMOTION:
            abspos = e.pos[0]+arect.x, e.pos[1]+arect.y
            for w in self.menu.container.widgets:
                if not w is self.menu:
                    mrect = w.get_abs_rect()
                    if mrect.collidepoint(abspos):
                        self.menu._close(None)
                        w._open(None)
                        handled = True

        elif e.type == EXIT:
            self.menu._close()

        if not handled: table.Table.event(self, e)

class Menu(button.Button):
    def __init__(self, parent, widget=None, **params): #TODO widget= could conflict with module widget
        params.setdefault('cls', 'menu')
        super(Menu, self).__init__(widget, **params)

        self.parent = parent

        self._cls = self.cls
        self.widgets = _Menu_Options(self, cls=self.cls+".options")

        self.connect(CLICK, self._open, None)

    def _open(self, w=None):
        self.parent.value = self
        self.pcls = 'down'

        self.repaint()
        self.container.open(self.widgets, self.rect.x, self.rect.bottom)
        self.widgets.connect(BLUR, self._close, None)
        self.widgets.focus()
        self.repaint()

    def _pass(self, w=None):
        pass

    def _close(self, w=None):
        self.pcls = ''
        self.parent.value = None
        self.repaint()
        self.widgets.close()
        self.send(EXIT)

    def _valuefunc(self, value):
        self._close(None)
        if value['fnc'] != None:
            if value['value']:
                value['fnc'](*value['value'])
            else:
                value['fnc']()

    def event(self, e):
        button.Button.event(self, e)

        if self.parent.value == self:
            self.pcls = 'down'

    # Modified for personal use
    def add(self, w, icon=None, fnc=None, value=None, **params):
        if isinstance(w, str): w += ' '

        params.setdefault("align", -1)
        w = button.Button(w, icon, cls=self.cls+".option", **params)
        w.connect(CLICK, self._valuefunc, {'fnc':fnc, 'value':value})

        self.widgets.tr()
        self.widgets.add(w)
        return w