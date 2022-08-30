from tkinter import Frame, Menu, IntVar, PhotoImage
from tkinter.dialog import Dialog
from tkinter.filedialog import asksaveasfilename

from sdl2 import SDL_CreateWindowFrom, SDL_FreeSurface
from sdl2.ext.window import Window

from os import getcwd
from webbrowser import open as open_link  # To open links in help menu
from datetime import datetime

# Internal
from .vars import *
from .draw import Draw

__all__ = ["Gui"]


class Gui:
  tkmaster = None
  paused = False

  def __init__(_, tkmaster, start_os, start_model):
    Gui.tkmaster = tkmaster

    Gui.header_frame = Frame(tkmaster, width=Constants.screen[0], height=Constants.head_size)
    Gui.header = Window('',(0,0))
    Gui.header.window = SDL_CreateWindowFrom(Gui.header_frame.winfo_id())

    Gui.screen_frame = Frame(tkmaster, width=Constants.screen[0], height=Constants.screen[1])
    Gui.screen = Window('',(0,0))
    Gui.screen.window = SDL_CreateWindowFrom(Gui.screen_frame.winfo_id())

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
    Gui.os_mode = IntVar(value=start_os[0] if 0 <= start_os[0] <= len(Config.os_list) else start_os[1])
    new = Menu(tearoff=False)
    for i, mode in enumerate(Config.os_list): new.add_radiobutton(label=mode["name"], variable=Gui.os_mode, value=i)
    Gui.menu.add_cascade(label="OS", menu=new)

    ## Model menu
    Gui.model_mode = IntVar(value=start_model[0] if 0 <= start_model[0] <= len(Config.model_list) else start_model[1])
    new = Menu(tearoff=False)
    for i, mode in enumerate(Config.model_list): 
      (new.add_radiobutton(label=mode["name"], variable=Gui.os_mode, value=i, state="disabled", activebackground="#F0F0F0") if mode.get("disabled", False) else 
       new.add_radiobutton(label=mode["name"], variable=Gui.os_mode, value=i))
    Gui.menu.add_cascade(label="Model", menu=new)

    ## Screenshot button
    Gui.menu.add_command(label="Screenshot", command=Gui.screenshot)

    ## Pause button
    Gui.menu.add_command(label="Pause ", )

    # Pack everything
    Gui.data = StateData()
    Gui.header_frame.pack()
    Gui.screen_frame.pack()

  def update_data():
    Gui.data(**Config.os_list[Gui.os_mode.get()], model=Config.model_list[Gui.model_mode.get()]["ratio"])

  def config(no_gui=False):
    if not Gui.tkmaster: raise RuntimeError("an instance must be created")

    # Set default data
    Gui.update_data()

    # Config window
    Gui.tkmaster.title(Constants.app_name)
    Gui.tkmaster.iconphoto(False, PhotoImage(file=Constants.path+"icons/emulator.png"))
    Gui.tkmaster.resizable(False, False)
    if not no_gui: Gui.tkmaster.config(menu=Gui.menu)
    Gui.tkmaster.eval('tk::PlaceWindow . center')

  def screenshot():
    Gui.paused = True # Pause events 
    file = (getcwd(), datetime.now().strftime("Screenshot_%m%d%Y-%H%M%S.png"))

    # Create new surface to blit head and screen into
    surf = Draw.new_surface(Constants.screen[0], Constants.head_size+Constants.screen[1])
    Draw.blit(surf, Gui.header.get_surface())
    Draw.blit(surf, Gui.screen.get_surface(), (0, Constants.head_size+1))
    
    try: ok = Config.save_image(surf, file[1])
    except: error = True
    else: error = ok != 0

    conf = {"title": "Screenshot", "text": "Screenshot savec at: \n"+'/'.join(file), "bitmap": "info", "default": 1, "strings":("Open folder", "OK")}
    if error: conf.update({"text": "Error, can't write in folder: \n"+file[0], "bitmap": "error", "strings":("Save as", "OK")})

    if not Dialog(Gui.tkmaster, conf).num:
      if error: 
        file = asksaveasfilename(defaultextension="png", filetypes=Constants.image_formats, initialfile=file[1], title="Save screenshot at")
        if file != '': Config.save_image(surf, file)
      else: open_link(file[0])
    
    SDL_FreeSurface(surf) # Remove surface from buffer
    Gui.paused = False # Screenshot finished, unpause events
