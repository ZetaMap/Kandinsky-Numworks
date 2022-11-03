# FAQ

### How to install PySDL2?
To install Pysdl2 and sdl2 library, open an sell and run: ``pip install pysdl2 pysdl2-dll``. If doesn't work, follow steps [here](https://pysdl2.readthedocs.io/en/latest/install.html).

### How to install this module?
To install this module, it's simple: open tan shell and run ``pip install kandinsky``. <br>
And if you want to run the [module demo](demo.py), run ``python -m kandinsky``. Normally a Snake game will launch and you could play it. =)

### Why convert colors?
Numworks works differently in color management, as its screen can only display **65,536** *(256/8\*256/4\*256/8)* colors compared to **16,000,000** colors for a regular screen. <br>
It is therefore necessary to make a conversion. To convert a color, you can use the function ``color()`` but you don't have to, by default the all methods does the conversions directly. <br>
**Example:** ``color(255, 255, 255) [White color] --> Return (248, 252, 248)``

### Why use external fonts?
To be as identical as possible to a result on the Numworks. <br>
You can find the fonts used [here](https://github.com/numworks/epsilon/tree/master/kandinsky/fonts).

### Why recreate the Numworks interface?
This can be useful, as it can serve as a guide for drawing.

### Why all functions are linked to a class?
To make the program more readable ("putting away your books allows you to find them more quickly"), and then I got used to programming like that (because of Java XD).

### Are you French ?
Yes, I'm French and my English is bad, that's why I use a translator XD.