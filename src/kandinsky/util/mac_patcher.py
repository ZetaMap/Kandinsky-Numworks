"""
Patch the module for MacOS. Redefine some methods of Core.

Since it's the only bone that doesn't accept the method I use to make a GUI,
it will try to patch the module to do a manual refresh.

This means that the program (if launched on this system) will have to regularly
call the display() method to refresh the window.

Basically using the same principle as in the first version of module
(when I was not using Threads yet)

Note: The window to notify the end of script to user, will be not available for mac
"""

from .core import Core, Gui, prettywarn

# Warning because library don't work on macos
prettywarn("no support of MacOS for moment. more infos here: "
           "https://github.com/ZetaMap/Kandinsky-Numworks/blob/pysdl2/FAQ.md#why-segfault-on-macos",
           ImportWarning)

# Global instance
Core_self: Core = None

def Core__init__(self: Core):
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

Core_event_fire_original = Core.event_fire
def Core_event_fire(self: Core, method, *args, **kwargs):
  """Wrapped method of .event_fire(), refresh the window after called the function"""
  value, err = Core_event_fire_original(self, method, *args, **kwargs)
  if not self.stopped: Gui.refresh()
  return value, err

def Core_is_alive(self: Core):
  """Redefine Thread.is_alive() to return always True, because the Thread never started and doesn't want errors about this"""
  return True

# Set new methods in Core
Core.__init__ = Core__init__
Core.event_fire = Core_event_fire
Core.is_alive = Core_is_alive

# And define the display method
def display():
  """Refresh manually the windows and display changes"""
  if Core_self is None:
    Gui.refresh() # unsafe
    return

  Core_self.refreshed = False
  _, err = Core_self.event_fire(Gui.refresh)
  Core_self.refreshed = True
  if err != None:
    raise err
