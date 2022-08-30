# FAQ

### How to install Pygame?
To install Pygame: open the [Command Prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/) and type: ``pip install pygame``. <br>
If don't work, write: ``py -m pip install pygame``. And if that still doesn't work, follow steps [here](https://docs.python.org/3/installing/index.html).

### How to install this module?
To install this module, it's simple: open the [Command Prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/) and type ``pip install kandinsky``. <br>
If don't work, type: ``py -m pip install kandinsky``. And if that still doesn't work, follow steps [here](https://docs.python.org/3/installing/index.html). <br>
And if you want to run the [module demo](demo.py), type ``py -m kandinsky`` in the Command Prompt. Normally a Snake game will launch and you could play it. =)

### Why Pygame and not Tkinter?
**Short description:** Pygame is a python module for making video games, it includes management of the camera, graphics, sound, etc. (more info [here](https://en.wikipedia.org/wiki/Pygame)). <br>
While Tkinter is more focused on managing windows (more info [here](https://en.wikipedia.org/wiki/Tkinter)). <br><br>
At first, I wanted to do this module on Tkinter, but a big problem bothered me. The window refresh took a very long time and consumes a lot of power. <br>
So I switched to Pygame because, seeing that this module is very well known, easy to use and made for creating games, the window refresh would necessarily be faster (a game that lags a lot, it is not very practical XD).

### What is display() for?
Windows works differently in window management.<br>
If you want to keep the window open, you will have to call the function ``display()`` at the end of your program, but it will block your program. To avoid this, you can use it with the argument True (``display(True)``) which will just refresh the screen without blocking the program. <br>
If you do not call this function, the window will appear at the beginning of your program and will close at the end of it.<br>

### Why convert colors?
Numworks works differently in color management, as its screen can only display **262,144** colors compared to **16,000,000** colors for a regular screen. <br>
It is therefore necessary to make a conversion. To convert a color, you can use the function ``color()`` but you don't have to because, by default, the module does the conversions directly. <br>
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