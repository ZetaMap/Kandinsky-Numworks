![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=ZetaMap.Kandinsky-Numworks) ![Downloads](https://shields.io/github/downloads/ZetaMap/Kandinsky-Numworks/total) ![pip](https://img.shields.io/pypi/dm/kandinsky?label=pip_downloads) ![GitHub Clones](https://img.shields.io/badge/dynamic/json?color=success&label=clones&query=count&url=https://gist.githubusercontent.com/ZetaMap/d3a3bcef3e64ffa553c11c173a444a97/raw/clone.json&logo=github)
# Kandinsky-Numworks
**This module depend to [PySDL2](https://pysdl2.readthedocs.io/en/latest/) module and sdl2 libraries, PySDL2 is just an [sdl2](https://www.libsdl.org/) wrapper with ctype and it just call methods in sdl2 library. To install both modules, click [here](https://github.com/ZetaMap/Kandinsky-Numworks/blob/pysdl2/FAQ.md#how-to-install-pysdl2) and follow steps.** <br>

This module allowing to link the kandinsky module, from the Numworks, to a window. Useful if you want to test your program without putting it on the calculator. <br>
In addition, this module also emulates the drawing speed, and has [many other features](https://github.com/ZetaMap/Kandinsky-Numworks/blob/pysdl2/README.md#additional-features).


### Installation
You now have the option to install this module on [pypi.org](https://pypi.org/project/kandinsky/). For that, follow the steps [here](https://github.com/ZetaMap/Kandinsky-Numworks/blob/pysdl2/FAQ.md#how-to-install-this-module).

Or if you want, you can build the module, just run command ``python builder.py``. <br>
This will be generate a setup.py, install module build, build library, and install it.

### More
I also recreated the ion module of the Numworks, check it out here: [Ion module of Numworks](https://github.com/ZetaMap/Ion-numworks)<br>
If you have a question, check out the [FAQ](https://github.com/ZetaMap/Kandinsky-Numworks/blob/pysdl2/FAQ.md). And if you have a suggestion or your question is not answered, open an [Issue](https://github.com/ZetaMap/Kandinsky-Numworks/issues/new).


### Usable content
#### ***Numworks, aka basic, methods***

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
* Parameters: ``text``, ``x``, ``y``, ``color`` **[default: (0,0,0)]**, ``background`` **[default: (248,252,248)]**, *(Omega & Upsilon only: ``font`` **[default: False]**)*
* Description: Display a text from pixel (x, y)
* Note: parameter ``font`` is only for Omega and Upsilon and it's to chose between small and large font.

**fill_rect():**
* Parameters: ``x``, ``y``, ``width``, ``height``, ``color``
* Description: Fill a rectangle at pixel (x, y)

#### ***New method for this library, only on Computer***

**quit():**
* Parameters: **No parameters**
* Description: Close manualy the window without notifying the user
* Note: after that you cannot reopen the window, so a re-import of kandinsky will be required to get a new window

**display():**
* Parameters: **No parameters**
* Description: Refresh manually the window and display changes
* Note: **⚠️Method added only for MacOS, because library cannot refresh automatically the window in another Thread. <br>
It will be necessary to call this method from time to time to keep it alive.⚠️**

#### ***New methods added by Omega (previous methods are also added)***

**draw_line()**
* Parameters: ``x1``, ``y1``, ``x2``, ``y2``, ``color``
* Description: Draw a line at (x1, y1) to (x2, y2)

**wait_vblank()**
* Parameters: **No parameters**
* Description: Wait for screen refresh

**get_keys()**
* Parameters: **No parameters**
* Description: Get name of pressed keys

#### ***New methods added by Upsilon (previous methods are also added except get_keys())***

**draw_circle()**
* Parameters: ``x``, ``y``, ``r``, ``color``
* Description: Draw circle at (x, y) of radius r

**fill_circle()**
* Parameters:  ``x``, ``y``, ``r``, ``color``
* Description: Fill circle at (x, y) of radius r

**fill_polygon()**
* Parameters: ``points``, ``color``
* Description: Fill polygon at points [(x1, y1), ...]

**get_palette()**
* Parameters: **No parameters**
* Description: Get theme palette


### Additional features
#### A GUI to control emulator

* **Pause/resume:** You can pause/resume your script <br> 
*Note:* This will just pause the calls of kandinsky. So for the script to pause, it must be called one of the functions of the library

* **Screenshot:** You can also take a screenshot of window <br>
*Note:* This take just the numworks interface and drawable area, not the GUI

* **Change OS:** Change the speed of execution. You have chose of **Numworks**, **Omega**, **Upsilon**, and **PC** mode <br>
*Note:* Only work for kandinsky methods

* **Change model:** Change the model of numworks. You have chose of **n0100**, **n0110**, and the new model **n0120** <br>
*Note:* This change the speed python execution emulation of numworks

* **Shorcut command:** All the features mentioned have a shortcut command. More info in the "Help" button of the window

#### Environ options
**/!\\ You must make its additions *before* importing kandinsky otherwise the changes will not take effect! /!\\**

You can also change some default option of library, like the OS or model on which to start kandinsky, etc. <br> 
To do this, first import the environ of os module like this: ``import os``.

* Enable debug mode:
```python
os.environ['KANDINSKY_ENABLE_DEBUG'] = '' 
```

* Change starting OS (methods according to the selected os will be created):
```python
# '0': PC speed + Upsilon methods
# '1': Numworks speed + Basic methods
# '2': Omega speed + draw_line,wait_vblank,get_keys method
# '3': Upsilon speed + draw_circle,fill_circle,fill_polygon,get_palette methods - get_keys
os.environ['KANDINSKY_OS_MODE'] = '<number>'
```

* Change starting Model:
```python
# '0': n0100 model speed (not available for moment)
# '1': n0110 model speed
# '2': n0120 model speed (not available for moment)
os.environ['KANDINSKY_MODEL_MODE'] = '<number>'
```

* Disable user interface (menu at top of window):
```python
# Note: Shortcut commands are not disabled
os.environ['KANDINSKY_NO_GUI'] = ''
```

* Change size of screen:
```python
os.environ['KANDINSKY_SCREEN_SIZE'] = "<width>x<height>"
```

* Zoom the screen:
```python
# from 1 to 4
os.environ['KANDINSKY_ZOOM_RATIO'] = "<number>"
```
