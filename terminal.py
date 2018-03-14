"""
Utilities for working with the terminal.

Functions:
* new_window(height, width, top, left, scrolling = True|False) - create a new window in the terminal

Constants:
* SCREEN_HEIGHT - the number of lines that fit on the screen
* SCREEN_WIDTH - the number of columns that fit on the screen
* NORMAL - used with the write function to produce normal text
* BOLD - used with the write function to produce bold text
* NEW_LINE - used with the write function to start a new line
"""
import curses

SCREEN_HEIGHT = curses.LINES
SCREEN_WIDTH = curses.COLS

BOLD = curses.A_BOLD
NORMAL = curses.A_NORMAL

NEW_LINE = '\n'

def new_window(height, width, top, left, scrolling = False):
    "Create a new window with the given dimensions."
    window = curses.newwin(height, width, top, left)
    window.immedok(True)  # update immediately
    window.scrollok(scrolling)
    return __wrap(window)

class Window():
    """
    A terminal window.

    Operations:
    * write(str, ..., style = NORMAL|BOLD) - write some text to a window
    * read(prompt) - read some text from the user
    * clear() - clear all text from the window
    """

    def __init__(self, window):
        self.__window = window

    def write(self, *objects, style = NORMAL):
        "Write text starting at the current position of the cursor."
        for obj in objects:
            self.__window.addstr(obj, style)

    def read(self, prompt = ''):
        "Read input from the user, with an optional prompt."
        self.write(prompt, style = BOLD)
        return self.__window.getstr().decode()

    def clear(self):
        self.__window.clear()

def __wrap(window):
    return Window(window)