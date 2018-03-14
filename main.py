import curses

def main(scr):
  curses.echo()
  import chat

curses.wrapper(main)