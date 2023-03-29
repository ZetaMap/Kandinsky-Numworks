from tkinter import Tk, Frame, Menu, IntVar
from tkinter.dialog import Dialog
from tkinter.filedialog import asksaveasfilename

from sdl2 import SDL_CreateWindowFrom, SDL_DestroyWindow, SDL_GetScancodeFromKey#, SDL_WINDOW_OPENGL
from sdl2.events import SDL_Event, SDL_PushEvent, SDL_KEYDOWN, SDL_PRESSED
from sdl2.ext import Window, load_image

from os import getcwd, system
from webbrowser import open as open_link, register_standard_browsers  # To open links in help menu
register_standard_browsers()
del register_standard_browsers
from datetime import datetime

# Internal
from .vars import *
from .draw import Draw

__all__ = ["Gui"]


class Gui:
  tkmaster:Tk = None
  paused = False
  already_paused = False

  def created():
    if not Gui.tkmaster: raise RuntimeError("an instance must be created")

  def __init__(_, tkmaster, start_os, start_model):
    Gui.tkmaster = tkmaster
    if not Constants.is_windows: Gui.tkmaster.option_add("*font", "SegoeUI 9")
    Gui.data = StateData()

    # Create frame area for sdl2 and pack it
    Gui.head_frame = Frame(tkmaster, width=Constants.screen[0], height=Constants.head_size)
    Gui.screen_frame = Frame(tkmaster, width=Constants.screen[0], height=Constants.screen[1])
    Gui.head_frame.pack()
    Gui.screen_frame.pack()
    Gui.screen_frame.focus_set()
    Gui.tkmaster.update()

    # OS head
    Gui.head = Window('',(0,0))
    SDL_DestroyWindow(Gui.head.window)
    Gui.head.window = SDL_CreateWindowFrom(Gui.head_frame.winfo_id())
    Gui.head_id = Gui.head_frame.winfo_id()
    
    # Drawable screen
    Gui.screen = Window('',(0,0))
    SDL_DestroyWindow(Gui.screen.window)
    Gui.screen.window = SDL_CreateWindowFrom(Gui.screen_frame.winfo_id())
    Gui.screen_id = Gui.screen_frame.winfo_id()

    Gui.menu = Menu(tkmaster)
    # Menus
    ## About menu
    about = Menu(tearoff=False)
    about.add_command(label="GitHub project",     command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks"))
    about.add_command(label="Documentation",      command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks#usable-content"))
    about.add_command(label="An issue? Open one", command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks/issues/new"))
    about.add_command(label="Made by ZetaMap",    command=lambda: open_link("https://github.com/ZetaMap"))
    Gui.menu.add_cascade(label="About", menu=about)

    ## Help menu
    help = Menu(tearoff=False)
    help.add_command(label="CTRL+O: change OS",       state="disabled", activebackground="#F0F0F0")
    help.add_command(label="CTRL+M: change Model",    state="disabled", activebackground="#F0F0F0")
    help.add_command(label="CTRL+S: take screenshot", state="disabled", activebackground="#F0F0F0")    
    help.add_command(label="CTRL+P: pause/resume",    state="disabled", activebackground="#F0F0F0")
    help.add_separator()
    help.add_command(label="Ion keyboard", command=lambda: open_link("https://github.com/ZetaMap/Ion-Numworks#keys"))
    help.add_command(label="Check FAQ",    command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md"))
    Gui.menu.add_cascade(label="Help", menu=help)

    ## OS menu
    max_ = len(Config.os_list)-1
    Gui.os_mode = IntVar(value=start_os[1] if start_os[0] < 0 or start_os[0] > max_ else start_os[0])
    new = Menu(tearoff=False)
    for i, mode in enumerate(Config.os_list): 
      new.add_radiobutton(label=mode["name"], variable=Gui.os_mode, value=i, command=Gui.update_data)
      Config.os_list[i]["battery"] = load_image(Constants.path+Config.os_list[i]["battery"])
    Gui.menu.add_cascade(label="OS", menu=new)

    ## Model menu
    max_ = len(Config.model_list)-1
    Gui.model_mode = IntVar(value=start_model[1] if start_model[0] < 0 or start_model[0] > max_ else start_model[0])
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
      Gui.already_paused = Gui.paused
      Gui.menu.entryconfig(6, label=["Pause", "Resume"][Gui.paused])
    Gui.menu.add_command(label="Pause", command=state,)

  def update_value(int_var, values):
    Gui.created()
    v = int_var.get()+1
    if v > len(values)-1: v = 0

    if not values[v].get("disabled", False):
      int_var.set(v)
      Gui.update_data()

  def update_data():
    Gui.created()
    if Gui.head.window is None: return

    Gui.data(**Config.os_list[Gui.os_mode.get()], model=Config.model_list[Gui.model_mode.get()]["ratio"])
    surf = Gui.head.get_surface()
    
    Draw.rect(surf, Gui.data.color)
    Draw.blit(surf, Config.small_font.render(Gui.data.unit), (5, 0))
    Draw.blit(surf, Config.small_font.render("PYTHON"), (Constants.screen[0]-181, 1))
    x = Constants.screen[0]-20  
    if Gui.data.clock:
      Draw.blit(surf, Config.small_font.render(datetime.now().strftime("%H:%M")), (x-20, 1))
      x -= 40
    Draw.blit(surf, Gui.data.battery, (x, 4))

  def config(no_gui=False):
    Gui.created()
    # Set default data
    Gui.update_data()

    # Config main window
    Gui.tkmaster.title(Constants.app_name)
    if Constants.is_windows: Gui.tkmaster.iconbitmap(default=Constants.path+"app.ico")
    else:
      from tkinter import PhotoImage
      Gui.tkmaster.iconphoto(True, PhotoImage(file=Constants.path+"app.png"))
    Gui.tkmaster.resizable(False, False)
    if not no_gui: Gui.tkmaster.config(menu=Gui.menu)
    Gui.tkmaster.eval('tk::PlaceWindow . center')

    # Bind shorcuts
    Gui.tkmaster.bind("<Control-o>", lambda _: Gui.update_value(Gui.os_mode, Config.os_list))
    Gui.tkmaster.bind("<Control-m>", lambda _: Gui.update_value(Gui.model_mode, Config.model_list))
    Gui.tkmaster.bind("<Control-s>", lambda _: Gui.screenshot())
    def state(_=None): 
      Gui.paused = not Gui.paused
      Gui.menu.entryconfig(6, label=["Pause", "Resume"][Gui.paused])
    Gui.tkmaster.bind("<Control-p>", state)

    # I don't know why, but i can't get focus of keyboard, so i will push keyboard events manually
    def on_key_press(event):
      sdl_event = SDL_Event(type=SDL_KEYDOWN)
      sdl_event.key.keysym.scancode = SDL_GetScancodeFromKey(event.keycode)
      sdl_event.key.keysym.sym = event.keycode+32
      sdl_event.key.state = SDL_PRESSED
      SDL_PushEvent(sdl_event)
    Gui.tkmaster.bind("<KeyPress>", on_key_press)

    # Clear sdl windows and refresh Tkinter frames
    Gui.refresh()

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
    
    try: error = Config.save_image(surf, file[1]) < 0
    except: error = 1

    conf = {"title": "Screenshot", "text": "Screenshot saved at: \n"+('\\' if Constants.is_windows else '/').join(file), "bitmap": "info", "default": 1, "strings": ("Open folder", "OK")}
    if error: conf.update({"text": "Error, can't write in folder: \n"+file[0], "bitmap": "error", "strings": ("Save as", "OK")})

    if not Dialog(Gui.tkmaster, conf).num:
      if error: 
        file = asksaveasfilename(defaultextension="png", filetypes=Constants.image_formats, initialfile=file[1], title="Save screenshot at")
        if file != '': 
          try: Config.save_image(surf, file)
          except: pass
      else: system(("explorer \"" if Constants.is_windows else "open \"")+file[0].replace('\\\\', '\\')+'"')

    del surf # destroy screenshot surface
    if not Gui.already_paused: Gui.paused = False # Screenshot finished, unpause events

  def askscriptend():
    return not Dialog(Gui.tkmaster, {
      "title": "Script end", "text": "Script finished! \nClose window?".ljust(50), 
      "bitmap": "question", "default": 0, "strings": ("Yes", "No")
    }).num
