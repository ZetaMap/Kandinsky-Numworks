from tkinter import Tk, Frame, Menu, IntVar, PhotoImage
from tkinter.dialog import Dialog
from tkinter.filedialog import asksaveasfilename

import warnings
warnings.filterwarnings('ignore', category=UserWarning) # Disable SDL warning 
from sdl2 import *
from sdl2.sdlimage import IMG_SavePNG_RW, IMG_Load, IMG_SaveJPG_RW, IMG_Init
from sdl2.ext import ttf, Window, Renderer, init, quit, draw, Texture

import os
from configparser import ConfigParser
from webbrowser import open as open_link, register_standard_browsers, register_X_browsers  # To open links in help menu
from datetime import datetime
from threading import Thread
from time import sleep

# Init some stuff
init()
IMG_Init(1)
IMG_Init(2)
register_standard_browsers()
register_X_browsers()

# Settings
class Vars:
  app_name = "KandinskyCore"
  path = os.path.dirname(__file__)+"/"
  image_formats = [("PNG", ".png"), ("Bitmap", ".bmp"), ("All files", ".*")]
  if os.name != "posix": image_formats.insert(1, ("JPEG", (".jpg", ".jpeg")))
  head_size = 19
  area = (320, 222)

# Load config


# Load fonts
class Fonts:
  small_font = ttf.FontManager(os.path.join(Vars.path, "fonts/small_font.ttf"), 12)
  large_font = ttf.FontManager(os.path.join(Vars.path, "fonts/large_font.ttf"), 16)  

# Cleanup namespaces
del warnings, init, IMG_Init, register_standard_browsers, register_X_browsers


# Define some methods
open = lambda path, mode="w": SDL_RWFromFile(path.encode("utf-8"), bytes(mode, "utf-8"))
save_image = lambda surface, path: (SDL_SaveBMP_RW(surface, open(path), 1) if path.endswith(".bmp") else 
                                    IMG_SaveJPG_RW(surface, open(path), 1, 80) if os.name != "posix" and path.endswith((".jpg", ".jpeg")) else
                                    IMG_SavePNG_RW(surface, open(path), 1))


# Define stuff
class Gui:
  tkmaster = None

  def __init__(_, tkmaster):
    Gui.tkmaster = tkmaster

    Gui.header = Frame(tkmaster, width=Vars.area[0], height=Vars.head_size)
    Gui.screen = Frame(tkmaster, width=Vars.area[0], height=Vars.area[1])
    Gui.header.pack()
    Gui.screen.pack()
    tkmaster.update()

    Gui.header_window = Window('',(0,0))
    Gui.header_window.window = SDL_CreateWindowFrom(Gui.header.winfo_id())
    Gui.header_renderer = Renderer(Gui.header_window)

    

    Gui.screen_window = Window('',(0,0))
    Gui.screen_window.window = SDL_CreateWindowFrom(Gui.screen.winfo_id())
    Gui.screen_renderer = Renderer(Gui.screen_window)

    
    Gui.menu = Menu(tkmaster)
    # Menus
    ## About menu
    new = Menu(tearoff=False)
    new.add_command(label="GitHub project",     command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks"))
    new.add_command(label="An issue? Open one", command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks/issues/new"))
    new.add_command(label="Made by ZetaMap",    command=lambda: open_link("https://github.com/ZetaMap"))
    Gui.menu.add_cascade(label="About", menu=new)

    ## Help menu
    new = Menu(tearoff=False)
    new.add_command(label="CTRL+O: change OS",       state="disabled", activebackground="#F0F0F0")
    new.add_command(label="CTRL+M: change Model",    state="disabled", activebackground="#F0F0F0")
    new.add_command(label="CTRL+P: pause/resume",    state="disabled", activebackground="#F0F0F0")
    new.add_command(label="CTRL+S: take screenshot", state="disabled", activebackground="#F0F0F0")
    new.add_separator()
    new.add_command(label="Check FAQ", command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks#usable-content"))
    Gui.menu.add_cascade(label="Help", menu=new)

    ## OS menu
    Gui.os_mode = IntVar(value=1)
    new = Menu(tearoff=False)
    new.add_radiobutton(label="PC",       variable=Gui.os_mode, value=0)
    new.add_radiobutton(label="Numworks", variable=Gui.os_mode, value=1)
    new.add_radiobutton(label="Omega",    variable=Gui.os_mode, value=2)
    new.add_radiobutton(label="Upsilon",  variable=Gui.os_mode, value=3)
    Gui.menu.add_cascade(label="OS", menu=new)

    ## Model menu
    Gui.model_mode = IntVar(value=1)
    new = Menu(tearoff=False)
    new.add_radiobutton(label="n0100", variable=Gui.model_mode, value=0, state="disabled", activebackground="#F0F0F0")
    new.add_radiobutton(label="n0110", variable=Gui.model_mode, value=1)
    new.add_radiobutton(label="n0120", variable=Gui.model_mode, value=2, state="disabled", activebackground="#F0F0F0")
    Gui.menu.add_cascade(label="Model", menu=new)

    ## Screenshot button
    Gui.menu.add_command(label="Screenshot", command=lambda: Gui.screenshot(Gui.screen_window.get_surface()))

    ## Pause button
    Gui.menu.add_command(label="Pause ", )

  def config():
    if not Gui.tkmaster: raise RuntimeError("an instance must be created")

    # More config
    Gui.tkmaster.title(Vars.app_name)
    Gui.tkmaster.iconphoto(False, PhotoImage(file=os.path.join(Vars.path, "icons/app.png")))
    Gui.tkmaster.resizable(False, False)
    Gui.tkmaster.config(menu=Gui.menu)
    Gui.tkmaster.eval('tk::PlaceWindow . center')
    
  def screenshot(surface):
    file = (os.getcwd(), datetime.now().strftime("Screenshot_%m%d%Y-%H%M%S.png"))
    
    try: ok = save_image(surface, file[1])
    except: error = True
    else: error = ok != 0

    if error: new = Dialog(Gui.tkmaster, {"title": "Screenshot", "text": "Error, can't write in folder: "+file[0], "bitmap": "error", "default":1, "strings":("Save as", "OK")})
    else: new = Dialog(Gui.tkmaster, {"title": "Screenshot", "text": "Screenshot savec at: "+os.path.join(*file), "bitmap": "info", "default":1, "strings":("Open folder", "OK")})

    if not new.num:
      if error: 
        path = asksaveasfilename(defaultextension="png", filetypes=Vars.image_formats, initialfile=file[1], title="Save screenshot at")
        print(path)
        if path != '': save_image(surface, path)
      else: open_link(file[0])


class Core(Thread):
  _loaded = False

  def __init__(self):
    super().__init__()
    self.start()

  def run(self):
    self.root = Tk()
    Gui(self.root)
    
    Gui.config()
    self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
    self.update()

    Core._loaded = True
    self.root.mainloop()

  def quit_app(self):
    del Gui.header_renderer, Gui.screen_renderer, Gui.header_window, Gui.screen_window
    quit()
    self.root.quit()

  def update(self):
    Gui.header_window.refresh()
    Gui.screen_window.refresh()
    self.root.after(100, self.update)
    


core = Core()
print("thread started, and waiting 2s")
sleep(2)
draw.fill(Gui.screen_window.get_surface(), "#fff", (10, 10, 100, 100))
sleep(2)
draw.fill(Gui.header_window.get_surface(), "#f00", (10, 10, 100, 5))
sleep(2)
SDL_BlitSurface(Fonts.large_font.render("test string", color="#f00", bg_color="#0f0"), None, Gui.screen_window.get_surface(), SDL_Rect(150, 150))
print("draw rect")