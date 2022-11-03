![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=ZetaMap.Kandinsky-Numworks) ![Downloads](https://shields.io/github/downloads/ZetaMap/Kandinsky-Numworks/total) ![pip](https://img.shields.io/pypi/dm/kandinsky?label=pip_downloads)
# Kandinsky-Numworks
**This module depend to [PySDL2](https://pysdl2.readthedocs.io/en/latest/) module and sdl2 libraries, PySDL2 is just an [sdl2](https://www.libsdl.org/) wrapper with ctype and it just call methods in sdl2 library. To install both modules, click [here](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md#how-to-install-pysdl2) and follow steps.** <br>

This module allowing to link the kandinsky module, from the Numworks, to a window. Useful if you want to test your program without putting it on the calculator. <br>
In addition, this module also emulates the drawing speed, and has [many other features](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/README.md#additional-features).

### Installation
You now have the option to install this module on [pypi.org](https://pypi.org/project/kandinsky/). For that, follow the steps [here](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md#how-to-install-this-module).

### More
I also recreated the ion module of the Numworks, check it out here: [Ion module of Numworks](https://github.com/ZetaMap/Ion-numworks)<br>
If you have a question, check out the [FAQ](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md). And if you have a suggestion or your question is not answered, open an [Issue](https://github.com/ZetaMap/Kandinsky-Numworks/issues/new).

### Usable content
**get_pixel()**:
* Parameters: ``x``, ``y``
* Description: Return pixel (x, y) color

**set_pixel():**
* Parameters: ``x``, ``y``, ``color``
* Description: Color pixel (x, y)

**color():**
* Parameters: ``r``, ``g``, ``b``
* Description: Define a rgb color

**draw_string():**
* Parameters: ``text``, ``x``, ``y``, ``color`` **[default: (0,0,0)]**, ``background`` **[default: (248,252,248)]**
* Description: Display a text from pixel (x, y)

**fill_rect():**
* Parameters: ``x``, ``y``, ``width``, ``height``, ``color``
* Description: Fill a rectangle at pixel (x, y)

**quit():**
* Parameters: **No parameters**
* Description: Close manualy the window without notifying the user
* Note: after that you cannot reopen the window, so a re-import of kandinsky will be required to get a new window.

### Additional features
A GUI to control library
* **Pause/resume:** You can pause/resume your script <br> 
*Note:* This will just pause the calls of kandinsky. So for the script to pause, it must be called one of the functions of the library

* **Screenshot:** You can also take a screenshot of screen <br>
*Note:* This take just the numworks interface and drawable area, not the GUI

* **Change OS:** Change the speed of execution. You have chose of **Numworks**, **Omega**, **Upsilon**, and **PC** mode <br>
*Note:* Only work for kandinsky methods

* **Change model:** Change the model of numworks. You have chose of **n0100**, **n0110**, and the new model **n0120** <br>
*Note:* This change the speed python execution emulation of numworks

* **Shorcut command:** All the features mentioned have a shortcut command. More info in the "Help" button of the window

Environ options <br>
**/!\\ You must make its additions *before* importing kandinsky otherwise the changes will not take effect! /!\\**

You can also change some default option of library, like the OS or model on which to start kandinsky, etc. <br> 
To do this, first import the environ of os module like this: ``import os``.

* To enable debug mode, add:
```python
os.environ['KANDINSKY_ENABLE_DEBUG'] = '' 
```

* To change starting OS, add:
```python
# '0': PC, '1': Numworks, '2': Omega, '3': Upsilon
os.environ['KANDINDKY_START_OS'] = '<number>'
```

* To change starting Model, add:
```python
# '0': n0100, '1': n0110, '2': n0120
os.environ['KANDINDKY_START_MODEL'] = '<number>'
```

* To disable user interface (menus at top of window), add:
```python
os.environ['KANDINSKY_NO_GUI'] = ''
```
