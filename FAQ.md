### How to install Pygame?
To install Pygame: open the [Command Prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/) and write: ``pip install pygame``.
If don't work, write: ``python -m pip install pygame``. And if that still doesn't work, follow steps [here](https://docs.python.org/3/installing/index.html).

### Why Pygame and not Tkinter?
**Short description:** <br>
Pygame is a python module for making video games, it includes management of the camera, graphics, sound, etc. (more info [here](https://fr.wikibooks.org/wiki/Pygame/Introduction_%C3%A0_Pygame)). While Tkinter is more focused on managing windows. <br><br>
At first, I wanted to do this module on Tkinter, but a big problem bothered me. The window refresh took a very long time and consumes a lot of power. <br>
So I switched to Pygame because, seeing that this module is very well known, easy to use and made for creating games, the window refresh would necessarily be faster (at the same time a game that lags a lot, it is not very practical XD).

### What is display() for?
Windows works differently in window management.<br>
If you want to keep the window open, you will have to call the function ``display()`` at the end of your program, but it will block your program. <br>
If you do not call this function, the window will appear at the beginning of your program and will close at the end of it.<br>

### Why convert colors?
Numworks works differently in color management, as its screen can only display **262,144** colors compared to **16,000,000** colors for a regular screen. <br>
It is therefore necessary to make a conversion. To convert a color, you can use the function ``color()`` but you don't have to because, by default, the module does the conversions directly. <br>
**Example:** ``color(255, 255, 255) [White color] --> Return (248, 252, 248)``


