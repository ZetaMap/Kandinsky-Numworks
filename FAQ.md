# FAQ

### How to install PySDL2?
To install Pysdl2 and sdl2 library, open an sell and run: ``pip install pysdl2 pysdl2-dll``. If doesn't work, follow steps [here](https://pysdl2.readthedocs.io/en/latest/install.html).

### How to install this module?
To install this module, it's simple: open tan shell and run ``pip install kandinsky``. <br>
And if you want to run the [module demo](demo.py), run ``python -m kandinsky``. Normally a Snake game will launch and you could play it. =)

### Why convert colors?
Numworks works differently in color management, as its screen can only display **65,536** *(256/8\*256/4\*256/8, 16 bits)* colors compared to **16,777,216** *(24 bits)* colors for a regular screen. <br>
It is therefore necessary to make a conversion. To convert a color, you can use the function ``color()`` but you don't have to, by default the all methods does the conversions directly. <br>
**Example:** ``color(255, 255, 255) [White color] --> Return (248, 252, 248)`` <br>
***Note for 'Numworks' mode:*** **Numworks added a feature to artificially expand color values, to make it look more natural. This feature has also been added, but the calculator screen can't show more colors, it's just a visual. Also feature not added for Omega and Upsilon**

### Why use external fonts?
To be as identical as possible to a result on the Numworks. <br>
You can find the fonts used [here](https://github.com/numworks/epsilon/tree/master/kandinsky/fonts).

### Why recreate the Numworks interface?
This can be useful, to help drawing or immersion.

### Why the library works differently than MacOS?
Because MacOS doesn't allow management of GUI by another Thread than the main Thread of program. <br>
Except precisely I need, not to occupy it, because otherwise that would block the program during importation of library, which thus does not have any more great interest. (¬_¬")<br>
**So for people on macOS, the ``display()`` function will have to be called regularly on operations not using library functions, to keep the window alive.**

### Why segfault on MacOS?
**Note: ignore that, it's solved! (the problem came from tkinter which gave false pointers)**

....Dude, idk....(* ￣︿￣) <br>
The error occurs when creating the SDL window from identifier of frame where it will be placed. <br>
So for the moment no MacOS support, even if I prepared the library for it ...

<details>
<summary>More details about error</summary>

The error occurs at line 154/155 in gui.py: <br>
![error1](https://github.com/ZetaMap/zetamap.github.io/blob/main/kandinsky-numworks/FAQ/error1.png?raw=true)

And the BackTrace from lldb: <br>
![error2](https://github.com/ZetaMap/zetamap.github.io/blob/main/kandinsky-numworks/FAQ/error2.png?raw=true)

So here is the information about the error for those who would like to help me fix it. <br>
You can offer me your fixs by creating a Pull Request.
<br>

</details>

### Are you French ?
Yes, I'm French and my English is bad, that's why I use a translator XD.