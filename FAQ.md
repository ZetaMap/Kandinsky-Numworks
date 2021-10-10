### How to install Pygame?
To install Pygame: open the [Command Prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/) and write: ``pip install pygame``.
If don't work, write: ``python -m pip install pygame``. And if that still doesn't work, follow steps [here](https://docs.python.org/3/installing/index.html).

### What is display() for?
Windows works differently in window management.<br>
If you want to keep the window open, you will have to call the function ``display()`` at the end of your program, but it will block your program. <br>
If you do not call this function, the window will appear at the beginning of your program and will close at the end of it.<br>
