import curses

# class Screen(object):
#     width = -1
#     height = -1

# screen = Screen()

def f(func):
    curses.echo()
    # setattr(screen, 'height', curses.LINES)
    # setattr(screen, 'width', curses.COLS)
    try:
        func(curses.LINES, curses.COLS)
    finally:
        pass

def run(func):
    curses.wrapper(lambda scr: f(func))

