### How to install Pygame?
To install Pygame: open the [Command Prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/) and write: ``pip install pygame``.
If don't work, write: ``python -m pip install pygame``. And if that still doesn't work, follow steps [here](https://docs.python.org/3/installing/index.html).

### What is display() for?
Windows works differently in window management.<br>
If you want to keep the window open, you will have to call the function ``display()`` at the end of your program, but it will block your program. <br>
If you do not call this function, the window will appear at the beginning of your program and will close at the end of it.<br>

### Why convert colors?
Numworks works differently in color management, as its screen can only display **262,144** colors compared to **16,000,000** colors for a regular screen. <br>
It is therefore necessary to make a conversion. To convert a color, you can use the function ``color()`` but you don't have to because, by default, the module does the conversions directly. <br>
**Example: ** ``color(255, 255, 255) [White color] --> Return (248, 252, 248)``
