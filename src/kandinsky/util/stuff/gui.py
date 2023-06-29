from tkinter import Tk, Frame, Menu, IntVar

from tkinter.dialog import Dialog
from tkinter.filedialog import asksaveasfilename
from tkinter.font import Font

from sdl2 import SDL_CreateWindowFrom, SDL_DestroyWindow, SDL_FreeSurface#, SDL_WINDOW_OPENGL
from sdl2.ext import Window, load_img, init

from os import getcwd, system
from webbrowser import open as open_link, register_standard_browsers  # To open links in help menu
register_standard_browsers() # register now to avoid a long wait when links open
del register_standard_browsers
from datetime import datetime

# Internal
from .vars import *
from .draw import Draw
from .color import Colors
from . import limiter

__all__ = ["Gui"]


class Gui:
  tkmaster:Tk = None
  paused = False
  already_paused = False
  drawable = None
  _main_thread_pid = None # because thread.native_pid don't exist in python<3.8, so use the other way
  heap_set = False

  def created():
    if not Gui.tkmaster: raise RuntimeError("Gui: an instance must be created")

  def _unpause_after_wrapper(method):
    def _wrap(*a, **k):
      method(*a, **k)
      if not Gui.already_paused: Gui.paused = False

    _wrap.__name__ = method.__name__
    return _wrap

  # Patched menu buttons to unpause script when is clicked
  _add_command = lambda menu, **kwargs: menu.add_command(**dict([(k, Gui._unpause_after_wrapper(v)) if "command" in k else (k, v) for k, v in kwargs.items()]))
  _add_radiobutton = lambda menu, **kwargs: menu.add_radiobutton(**dict([(k, Gui._unpause_after_wrapper(v)) if "command" in k else (k, v) for k, v in kwargs.items()]))

  def __init__(_, tkmaster):
    # This is now, the video subsystem of SDL will be initialized
    init(video=True)

    Gui.tkmaster = tkmaster
    if Vars.is_linux:
      Gui.linux_menu_font = Font(tkmaster, family="SegoeUI", size=9)
      Gui.tkmaster.option_add("*font", Gui.linux_menu_font)
    Gui.data = StateData()

    # Create frame area, sdl2 windows and pack everything
    Gui.head_frame = Frame(tkmaster)
    Gui.screen_frame = Frame(tkmaster)
    Gui.head_frame.pack()
    Gui.screen_frame.pack()
    Gui.tkmaster.update()
    Gui.head = Window('',(0,0))
    Gui.screen = Window('',(0,0))

    Gui.menu = Menu(tkmaster)
    # Menus
    ## Help menu
    about = Menu(tearoff=False)
    Gui._add_command(about, label="GitHub project",     command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks"))
    Gui._add_command(about, label="Documentation",      command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks#usable-content"))
    Gui._add_command(about, label="An issue? Open one", command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks/issues/new"))
    Gui._add_command(about, label="Made by ZetaMap",    command=lambda: open_link("https://github.com/ZetaMap"))
    Gui.menu.add_cascade(label="About", menu=about)

    ## Help menu
    help = Menu(tearoff=False)
    sortcut = Menu(tearoff=False)

    Gui._add_command(sortcut, label="CTRL+Q: Close window",    state="disabled", activebackground="#F0F0F0")
    Gui._add_command(sortcut, label="CTRL+O: change OS",       state="disabled", activebackground="#F0F0F0")
    Gui._add_command(sortcut, label="CTRL+M: change Model",    state="disabled", activebackground="#F0F0F0")
    Gui._add_command(sortcut, label="CTRL+S: take screenshot", state="disabled", activebackground="#F0F0F0")
    Gui._add_command(sortcut, label="CTRL+P: pause/resume",    state="disabled", activebackground="#F0F0F0")
    Gui._add_command(sortcut, label="CTRL+Z: change zoom",     state="disabled", activebackground="#F0F0F0")
    help.add_cascade(label="Shortcut", menu=sortcut)

    help.add_separator()
    Gui._add_command(help, label="Ion keyboard", command=lambda: open_link("https://github.com/ZetaMap/Ion-Numworks#associated-keyboard-keys"))
    Gui._add_command(help, label="Check FAQ",    command=lambda: open_link("https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md"))
    Gui.menu.add_cascade(label="Help", menu=help)

    ## Options menu
    Gui.options = Menu(tearoff=False)

    ## OS menu
    Gui.os_mode = IntVar(value=Vars.selected_os)
    new = Menu(tearoff=False)
    for i, mode in enumerate(Config.os_list):
      Gui._add_radiobutton(new, label=mode["name"], variable=Gui.os_mode, value=i, command=Gui.update_data)
      Config.os_list[i]["battery"] = load_img(Vars.path+Config.os_list[i]["battery"])
    Gui.options.add_cascade(accelerator="CTRL+O", label="OS", menu=new)

    ## Model menu
    Gui.model_mode = IntVar(value=Vars.selected_model)
    new = Menu(tearoff=False)
    for i, mode in enumerate(Config.model_list):
      Gui._add_radiobutton(new, label=mode["name"], variable=Gui.model_mode, value=i, command=Gui.update_data,
        **({"state": "disabled", "activebackground": "#F0F0F0"} if mode.get("disabled", False) else {}))
    Gui.options.add_cascade(accelerator="CTRL+M", label="Model", menu=new)

    Gui.zoom = IntVar(value=Vars.zoom_ratio)
    Gui.increase_font = IntVar()
    Gui.zoom.trace_add("write", Gui.set_zoom)
    Gui.increase_font.trace_add("write", Gui.set_zoom)
    new = Menu(tearoff=False)
    for i in range(Config.zoom_max): Gui._add_radiobutton(new, label=f"x{i+1}", variable=Gui.zoom, value=i+1)
    if Vars.is_linux: new.add_checkbutton(label="Increase font size", variable=Gui.increase_font)
    Gui.options.add_cascade(accelerator="CTRL+Z", label="Zoom", menu=new)

    Gui.options.add_separator()

    ## Screenshot button
    Gui.options.add_command(accelerator="CTRL+S", label="Screenshot", command=Gui.askscreenshot)

    ## Pause button
    def state(states=["Pause", "Resume"]):
      Gui.already_paused = not Gui.already_paused
      Gui.paused = Gui.already_paused
      Gui.options.entryconfig(states[not Gui.already_paused], label=states[Gui.already_paused])
    Gui.options.add_command(accelerator="CTRL+P", label="Pause", command=state)

    Gui.menu.add_cascade(label="Options", menu=Gui.options)

  def set_zoom(*_, force=False):
    Gui.created()

    Gui.paused = True # Give time to change var, destroy and rebuild window
    last_zoom = Vars.zoom_ratio
    Vars.zoom_ratio = Gui.zoom.get()
    if Vars.is_linux: Gui.linux_menu_font.config(size=9*(Vars.zoom_ratio if Gui.increase_font.get() else 1))

    if not force and last_zoom == Vars.zoom_ratio:
      # No need to continue
      if not Gui.already_paused: Gui.paused = False
      return

    SDL_DestroyWindow(Gui.head.window)
    SDL_DestroyWindow(Gui.screen.window)
    Gui.head_frame.config(width=Vars.screen[0]*Vars.zoom_ratio, height=Vars.head_size*Vars.zoom_ratio)
    Gui.screen_frame.config(width=Vars.screen[0]*Vars.zoom_ratio, height=Vars.screen[1]*Vars.zoom_ratio)
    Gui.tkmaster.update()
    Gui.head.window = SDL_CreateWindowFrom(Gui.head_frame.winfo_id())
    Gui.screen.window = SDL_CreateWindowFrom(Gui.screen_frame.winfo_id())
    Gui.screen_surf = Gui.screen.get_surface()

    last_drawable = Gui.drawable
    Gui.drawable = Draw.new_surface(*Vars.screen)
    Draw.rect(Gui.drawable, Colors.fix2(Colors.white))
    Draw.blit_scaled(Gui.drawable, last_drawable)
    Gui.update_data()

    Gui.center_window()
    if not Gui.already_paused: Gui.paused = False

  def destroy():
    Gui.created()

    SDL_FreeSurface(Gui.drawable)
    Gui.head.close()
    Gui.screen.close()
    Gui.tkmaster.quit()
    Gui.tkmaster = None

  def update_value(int_var, values, min=0):
    Gui.created()
    v = int_var.get()+1
    if v > len(values)-1: v = min

    if not values[v].get("disabled", False):
      int_var.set(v)
      Gui.update_data()

  def update_data():
    Gui.created()
    if Gui.head.window is None: return

    Gui.data(**Config.os_list[Gui.os_mode.get()], model=Config.model_list[Gui.model_mode.get()]["ratio"])
    Gui.head_surface = Draw.new_surface(Vars.screen[0],Vars.head_size)

    Draw.rect(Gui.head_surface, Gui.data.color)
    Draw.string(Gui.head_surface, Config.small_font, Gui.data.unit, 5, 0)
    Draw.string(Gui.head_surface, Config.small_font, "PYTHON", Vars.screen[0]//2-21, 1)
    x = Vars.screen[0]-20
    if Gui.data.clock:
      Draw.string(Gui.head_surface, Config.small_font, datetime.now().strftime("%H:%M"), x-20, 1)
      x -= 40
    Draw.blit_scaled(Gui.head_surface, Gui.data.battery, (x, 4))
    # try to blit it now on screen
    try: Draw.blit(Gui.head.get_surface(), Gui.head_surface)
    except: pass

    # Set new heap of python
    if Gui._main_thread_pid:
      try: limiter.set_heap(Gui._main_thread_pid, Gui.data.heap)
      except (AssertionError, OSError): raise #Gui.heap_set = False
      else: Gui.heap_set = True

  def config(create_gui=False):
    Gui.created()

    # Config main window
    Gui.tkmaster.title(Vars.app_name)
    if Vars.is_windows: Gui.tkmaster.iconbitmap(default=Vars.path+"app.ico")
    else:
      from tkinter import PhotoImage
      Gui.tkmaster.iconphoto(True, PhotoImage(file=Vars.path+"app.png"))
    Gui.tkmaster.resizable(False, False)
    if create_gui: Gui.tkmaster.config(menu=Gui.menu)
    Gui.tkmaster.eval('tk::PlaceWindow . center') # I must keep this otherwise the SDL windows do not configure correctly
    Gui.center_window()

    # Bind shorcuts
    Gui.tkmaster.bind("<Control-o>", lambda _: Gui.update_value(Gui.os_mode, Config.os_list))
    Gui.tkmaster.bind("<Control-m>", lambda _: Gui.update_value(Gui.model_mode, Config.model_list))
    Gui.tkmaster.bind("<Control-s>", lambda _: Gui.askscreenshot())
    def state(*_, states=["Pause", "Resume"]):
      Gui.already_paused = not Gui.already_paused
      Gui.paused = Gui.already_paused
      Gui.options.entryconfig(states[not Gui.already_paused], label=states[Gui.already_paused])
    Gui.tkmaster.bind("<Control-p>", state)
    Gui.tkmaster.bind("<Control-z>", lambda _: Gui.update_value(Gui.zoom, [{}]*(Config.zoom_max+1), 1))

    ### Windows patchs
    if Vars.is_windows:
      # Bind events to pause, if dragged or user interact with gui
      def drag_event(e):
        if e.widget is Gui.tkmaster:
          if Gui._drag_window_event_id:
            Gui.tkmaster.after_cancel(Gui._drag_window_event_id)
            Gui.paused = True
          Gui._drag_window_event_id = Gui.tkmaster.after(200, drag_event_stop)
      def drag_event_stop():
        Gui._drag_window_event_id = ''
        if not Gui.already_paused: Gui.paused = False
      drag_event_stop()
      Gui.tkmaster.bind("<Configure>", drag_event)

      # Pause on opening menu and unpause when click on frames
      def pause(*_): Gui.paused = True
      unpause = Gui._unpause_after_wrapper(lambda *_: None)

      Gui.menu["postcommand"] = pause
      Gui.head_frame.bind("<Button-1>", unpause)
      Gui.screen_frame.bind("<Button-1>", unpause)
    ###

    Gui.set_zoom(force=True) # Force set zoom of window
    Gui.update_data() # Set default data
    Gui.refresh() # Refresh SDL windows and Tkinter frames

  def center_window():
    Gui.created()
    Gui.tkmaster.geometry(f"+{max(0, Gui.tkmaster.winfo_screenwidth() //2-Gui.tkmaster.winfo_width() //2)}"
                          f"+{max(0, Gui.tkmaster.winfo_screenheight()//2-Gui.tkmaster.winfo_height()//2)}")

  def refresh():
    Gui.created()

    Gui.head.refresh()
    Draw.rect(Gui.screen_surf, Colors.black)
    Draw.blit(Gui.screen_surf, Gui.drawable)
    Gui.screen.refresh()
    Gui.tkmaster.update_idletasks()
    Gui.tkmaster.update()

  def askscreenshot():
    Gui.created()
    Gui.paused = True # Pause events
    file = (getcwd().replace("\\\\", "\\"), datetime.now().strftime("Screenshot_%Y%m%d-%H%M%S.png"))

    # Create new surface to blit head and screen into
    surf = Draw.new_surface(Vars.screen[0], Vars.head_size+Vars.screen[1])
    Draw.blit(surf, Gui.head_surface)
    Draw.blit(surf, Gui.drawable, (0, Vars.head_size))

    try: error = Config.save_image(surf, file[1]) < 0
    except: error = 1

    conf = {"title": "Screenshot", "text": "Screenshot saved at: \n"+('\\' if Vars.is_windows else '/').join(file), "bitmap": "info", "default": 1, "strings": ("Open folder", "OK")}
    if error: conf.update({"text": "Error, can't write in folder: \n"+file[0], "bitmap": "error", "strings": ("Save as", "OK")})

    if not Dialog(Gui.tkmaster, conf).num:
      if error:
        file = asksaveasfilename(defaultextension="png", filetypes=Vars.image_formats, initialfile=file[1], title="Save screenshot at")
        if file != '':
          try: Config.save_image(surf, file)
          except: pass
      else: system(f"{'explorer' if Vars.is_windows else 'open' if Vars.is_macos else 'xdg-open'} \"{file[0]}\" 2> {'nul' if Vars.is_windows else '/dev/null'}")

    SDL_FreeSurface(surf) # destroy screenshot surface
    if not Gui.already_paused: Gui.paused = False # Screenshot finished, unpause events

  def askscriptend():
    return not Dialog(Gui.tkmaster, {
      "title": "Script end", "text": "Script finished! \nClose window?".ljust(50),
      "bitmap": "question", "default": 0, "strings": ("Yes", "No")
    }).num
