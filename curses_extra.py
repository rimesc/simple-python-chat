import curses

BOLD = curses.A_BOLD
NORMAL = curses.A_NORMAL

NEW_LINE = '\n'

def write(window, *objects, style = NORMAL):
    "Write text starting at the current position of the cursor."
    for obj in objects:
        window.addstr(obj, style)

def f(func):
    curses.echo()
    try:
        func(curses.LINES, curses.COLS)
    finally:
        pass

def run(func):
    curses.wrapper(lambda scr: f(func))
