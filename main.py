import curses

def main(scr):
  curses.echo()
  curses.start_color()
  curses.use_default_colors()
  for i in range(0, curses.COLORS):
    curses.init_pair(i + 1, i, -1)
  import chat

curses.wrapper(main)