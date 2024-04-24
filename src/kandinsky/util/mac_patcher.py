"""
Patch the module for MacOS. Redefine some methods of Core and Gui classes.

Since it's the only bone that doesn't accept the method I use to make a GUI,
it will try to patch the module to do a manual refresh.

This means that the program (if launched on this system) will have to regularly
call the display() method to refresh the window.

Basically using the same principle as in the first version of module
(when I was not using Threads yet)

Note: The window to notify the end of script to user, will be not available for mac
"""

from .core import Core, Gui, Vars, Draw, Colors

# Global instance
Core_self: Core = None

def Core___init__(self: Core):
    """Patched version of core, this will not start the Thread and just init library"""
    global Core_self # global instance for display function
    Core_self = self

    Gui.paused = Gui.already_paused = True

    # Stop module to avoid entering in main loop
    self.stopped = True
    # Init module
    self.event_loop()
    # And module is now available
    self.stopped = False

Core_event_fire_ = Core.event_fire
def Core_event_fire(self: Core, method, *args, **kwargs):
  """Wrapped method of .event_fire(), refresh the window after called the function"""
  value, err = Core_event_fire_(self, method, *args, **kwargs)
  if not self.stopped: Gui.refresh()
  return value, err

def Core_is_alive(self: Core):
  """Redefine Thread.is_alive() to return always True, because the Thread never started and we don't want errors about this"""
  return True


# Set new methods in Core
Core.__init__ = Core___init__
Core.event_fire = Core_event_fire
Core.is_alive = Core_is_alive


# And define the display method
def display():
  """Refresh manually the window and display changes"""
  if Core_self is None:
    Gui.refresh() # unsafe
    return

  Core_self.refreshed = False
  _, err = Core_self.event_fire(Gui.refresh)
  Core_self.refreshed = True
  if err != None:
    raise err


# Also I don't know why, but tkinter give wrong widget id, so let's patch this
# to install: pyobjc-core pyobjc-framework-Cocoa
try: from objc import pyobjc_id
except ImportError as e:
  e.msg = "'pyobjc' module and his Cocoa framework is needed for your platform. Please install it with command 'pip3 install pyobjc-core pyobjc-framework-Cocoa'"
  raise

def Gui_get_widget_id(widget):
  """
  Returns the main window, not the widget frame because a can't get the widget with 'objc', there is nothing on web.
  Literally nobody has this problem, and no AI can solve my problem.

  So to avoid overlapping SDL windows, I'm going to offset them myself when refreshing
  """
  from AppKit import NSApp
  return pyobjc_id(NSApp.windows()[-1].contentView())

def Gui_refresh():
  """Offset drawable surface on screen"""
  Gui.created()

  Draw.rect(Gui.screen_surf, Colors.black)
  Draw.blit(Gui.screen_surf, Gui.head_surface)
  Draw.blit(Gui.screen_surf, Gui.drawable, (0, Vars.head_size))
  Gui.screen.refresh()
  Gui.tkmaster.update_idletasks()
  Gui.tkmaster.update()

# Set new methods in Gui
Gui.get_widget_id = Gui_get_widget_id
Gui.refresh = Gui_refresh
