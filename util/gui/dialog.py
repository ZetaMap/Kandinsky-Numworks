"""
"""
from .const import *
from . import table, button, basic

# Modified for personal use
class Dialog(table.Table):
    """A dialog window with a title bar and an "close" button on the bar.
    
    Example:
        title = gui.Label("My Title")
        main = gui.Container()
        #add stuff to the container...
        
        d = gui.Dialog(title,main)
        d.open()

    """
    _main = None

    def __init__(self,title,main,**params):
        """Dialog constructor.

        Arguments:
            title -- title widget, usually a label
            main -- main widget, usually a container

        """        
        params.setdefault('cls','dialog')
        super(Dialog, self).__init__(**params)
        
        if type(title) == str: self.title = basic.Label(title, align=-1, cls=self.cls+'.title.label')
        self.td(self.title,align=-1,cls=self.cls+'.bar')
        self.clos = button.Icon(self.cls+".bar.close")
        self.clos.connect(CLICK,self.close,None) 
        self.td(self.clos,align=1,cls=self.cls+'.bar')
        
        self.tr()
        self._main = main
        self.td(self._main,colspan=2,cls=self.cls+".main")

    def set_main(self, main):
        self.remove(self._main)
        
        self._main = main
        self.td(self._main,colspan=2,cls=self.cls+".main")

        self.chsize()