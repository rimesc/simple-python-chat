import curses

from curses import newwin
from curses_extra import run

def main(screen_height, screen_width):
    log_window = newwin(screen_height - 2, screen_width, 0, 0)
    log_window.scrollok(True)  # when the window is full, scroll old messages off the top
    log_window.immedok(True)  # update immediately when a new message arrives

    input_window = newwin(2, screen_width, screen_height-2, 0)
    input_window.hline(curses.ACS_HLINE, screen_width)
    input_window.addstr(1, 0, 'Write a message:')
    input_window.refresh()
    while True:
        input_window.move(1, 17)
        input_window.clrtoeol()  # clear the input area ready for a new message
        message = input_window.getstr(screen_width - 17)

        log_window.addstr(message + '\n')

run(main)
