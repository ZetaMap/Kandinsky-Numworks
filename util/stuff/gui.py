from tkinter import Tk, Frame, Menu, IntVar
from tkinter.dialog import Dialog
from tkinter.filedialog import asksaveasfilename

from sdl2 import SDL_CreateWindowFrom
from sdl2.ext import Window, load_image

from os import getcwd
from webbrowser import open as open_link  # To open links in help menu
from datetime import datetime

# Internal
from .vars import *
from .draw import Draw

__all__ = ["Gui"]


class Gui:
  tkmaster:Tk = None
  paused = False

  def created():
    if not Gui.tkmaster: raise RuntimeError("an instance must be created")

  def __init__(_, tkmaster, start_os, start_model):
    Gui.tkmaster = tkmaster

    # Create frame area for sdl2
    Gui.head_frame = Frame(tkmaster, width=Constants.screen[0], height=Constants.head_size)
    Gui.screen_frame = Frame(tkmaster, width=Constants.screen[0], height=Constants.screen[1])
    Gui.head_frame.pack()
    Gui.screen_frame.pack()
    tkmaster.update()

    # OS head
    Gui.head = Window('',(0,0))
    Gui.head.window = SDL_CreateWindowFrom(Gui.head_frame.winfo_id())
    
    # Drawable screen
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
    new.add_command(label="CTRL+S: take screenshot", state="disabled", activebackground="#F0F0F0")    
    new.add_command(label="CTRL+P: pause/resume",    state="disabled", activebackground="#F0F0F0")
    new.add_separator()
    new.add_command(label="Check FAQ", command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks#usable-content"))
    Gui.menu.add_cascade(label="Help", menu=new)

    ## OS menu
    max = len(Config.os_list)
    Gui.os_mode = IntVar(value=start_os[0] if 0 <= start_os[0] <= max else start_os[1])
    new = Menu(tearoff=False)
    for i, mode in enumerate(Config.os_list): 
      new.add_radiobutton(label=mode["name"], variable=Gui.os_mode, value=i, command=Gui.update_data)
      Config.os_list[i]["head"] = load_image(Constants.path+Config.os_list[i]["head"])
    Gui.menu.add_cascade(label="OS", menu=new)

    ## Model menu
    max = len(Config.model_list)
    Gui.model_mode = IntVar(value=start_model[0] if 0 <= start_model[0] <= max else start_model[1])
    new = Menu(tearoff=False)
    for i, mode in enumerate(Config.model_list): 
      new.add_radiobutton(label=mode["name"], variable=Gui.model_mode, value=i, command=Gui.update_data, 
                          **({"state": "disabled", "activebackground": "#F0F0F0"} if mode.get("disabled", False) else {}))
    Gui.menu.add_cascade(label="Model", menu=new)

    ## Screenshot button
    Gui.menu.add_command(label="Screenshot", command=Gui.screenshot)

    ## Pause button
    def state(): 
      Gui.paused = not Gui.paused
      Gui.menu.entryconfig(6, label=["Pause", "Resume"][Gui.paused])
    Gui.menu.add_command(label="Pause", command=state,)

    # Pack everything
    Gui.data = StateData()

  def update_value(int_var, max):
    Gui.created()
    int_var.set(int_var.get()+1)
    if int_var.get() > max: int_var.set(0)
    
    Gui.update_data()

  def update_data():
    Gui.created()
    #print(Gui.data)
    Gui.data(**Config.os_list[Gui.os_mode.get()], model=Config.model_list[Gui.model_mode.get()]["ratio"])
    surf = Gui.head.get_surface()
    Draw.rect(surf, Gui.data.color)
    Draw.blit(surf, Gui.data.head)

  def config(no_gui=False):
    Gui.created()
    # Set default data
    Gui.update_data()

    # Config main window
    Gui.tkmaster.title(Constants.app_name)
    Gui.tkmaster.iconbitmap(False, Constants.path+"app.ico")
    Gui.tkmaster.resizable(False, False)
    if not no_gui: Gui.tkmaster.config(menu=Gui.menu)
    Gui.tkmaster.eval('tk::PlaceWindow . center')

    # Clear sdl windows
    Gui.refresh()

    # Bind shorcuts
    Gui.tkmaster.bind("<Control-o>", lambda _: Gui.update_value(Gui.os_mode, len(Config.os_list)-1))
    Gui.tkmaster.bind("<Control-m>", lambda _: Gui.update_value(Gui.model_mode, len(Config.model_list)-1))
    Gui.tkmaster.bind("<Control-s>", lambda _: Gui.screenshot())
    def state(_=None): 
      Gui.paused = not Gui.paused
      Gui.menu.entryconfig(6, label=["Pause", "Resume"][Gui.paused])
    Gui.tkmaster.bind("<Control-p>", state)

  def refresh():
    Gui.created()
    
    Gui.tkmaster.update_idletasks()  
    Gui.tkmaster.update()
    Gui.head_frame.update()
    Gui.screen_frame.update()

  def screenshot():
    Gui.created()
    Gui.paused = True # Pause events 
    file = (getcwd(), datetime.now().strftime("Screenshot_%Y%m%d-%H%M%S.png"))

    # Create new surface to blit head and screen into
    surf = Draw.new_surface(Constants.screen[0], Constants.head_size+Constants.screen[1])
    Draw.blit(surf, Gui.head.get_surface())
    Draw.blit(surf, Gui.screen.get_surface(), (0, Constants.head_size))
    
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
    
    del surf # Use finish so destroy it
    Gui.paused = False # Screenshot finished, unpause events
