![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=ZetaMap.Kandinsky-Numworks) ![Downloads](https://shields.io/github/downloads/ZetaMap/Kandinsky-Numworks/total) ![pip](https://img.shields.io/pypi/dm/kandinsky?label=pip_downloads) ![GitHub Clones](https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count&url=https://gist.githubusercontent.com/ZetaMap/d3a3bcef3e64ffa553c11c173a444a97/raw/clone.json&logo=github)
# Kandinsky-Numworks
**This module depend to [Pygame](https://fr.wikibooks.org/wiki/Pygame/Introduction_%C3%A0_Pygame) module. To install it, click [here](https://github.com/ZetaMap/Kandinsky-Numworks/blob/main/FAQ.md#how-to-install-pygame) and follow steps.** <br>
A small module allowing to link the kandinsky module, from the Numworks, to a window. 
Useful if you want to test your program without putting it on the calculator. <br>

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
