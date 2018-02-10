import curses

def f(func):
    curses.echo()
    try:
        func(curses.LINES, curses.COLS)
    finally:
        pass

def run(func):
    curses.wrapper(lambda scr: f(func))

