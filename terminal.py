"""
Utilities for working with the terminal.

Functions:
* run(main_program) - run the main program
* new_window(height, width, top, left, scrolling = True|False) - create a new window in the terminal
* write(window, 'some', 'text', style = NORMAL|BOLD) - write some text to a window
* read(window, prompt='enter: ') - read some text from the user

Constants:
* NORMAL - used with the write function to produce normal text
* BOLD - used with the write function to produce bold text
* NEW_LINE - used with the write function to start a new line
"""

import curses

BOLD = curses.A_BOLD
NORMAL = curses.A_NORMAL

NEW_LINE = '\n'

def new_window(height, width, top, left, scrolling = False):
    "Create a new window with the given dimensions."
    window = curses.newwin(height, width, top, left)
    window.immedok(True)  # update immediately
    window.scrollok(scrolling)
    return window

def write(window, *objects, style = NORMAL):
    "Write text starting at the current position of the cursor."
    for obj in objects:
        window.addstr(obj, style)

def read(window, prompt = ''):
    "Read input from the user, with an optional prompt."
    write(window, prompt, style = BOLD)
    return window.getstr().decode()

def __f(func):
    curses.echo()
    try:
        func(curses.LINES, curses.COLS)
    finally:
        pass

def run(func):
    curses.wrapper(lambda scr: __f(func))
