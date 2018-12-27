import curses

def main(scr):
  curses.echo()
  curses.start_color()
  curses.use_default_colors()
  import chat

curses.wrapper(main)