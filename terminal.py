"""
Utilities for working with the terminal.

Splits the terminal into two parts - a scrolling message log and a user input
box - and provides facades for accessing the two parts.

Members:
* message_log - the message log
* input_box - the input box
* NORMAL - style constant used with the write function to produce normal text
* BOLD - style constant used with the write function to produce bold text
* NEW_LINE - the new line character
* MAX_LINES - constant containing the height of the terminal in lines of text
* MAX_COLS - constant containing the width of the terminal in columns of text
"""
import curses

MAX_LINES = curses.LINES  # pylint: disable=no-member
MAX_COLS = curses.COLS    # pylint: disable=no-member

BOLD = curses.A_BOLD
NORMAL = curses.A_NORMAL

NEW_LINE = '\n'

__mainwindow = curses.newwin(MAX_LINES, MAX_COLS, 0, 0)
__mainwindow.immedok(True)  # update immediately
__mainwindow.hline(MAX_LINES - 2, 0, curses.ACS_HLINE, MAX_COLS)

# divide the main window into a scrolling chat log and an input box for typing messages

_logwindow = __mainwindow.subwin(MAX_LINES - 2, MAX_COLS, 0, 0)
_logwindow.immedok(True)  # update immediately
_logwindow.scrollok(True)

_inputwindow = __mainwindow.subwin(1, MAX_COLS, MAX_LINES - 1, 0)
_inputwindow.immedok(True)  # update immediately

class MessageLog(object):

  def print(self, *objects, style = NORMAL):
    "Write text starting at the current position of the cursor."
    for obj in objects:
      _logwindow.addstr(obj, style)
    _inputwindow.addstr('') # return focus to the input window

  def clear(self):
    "Clear the window."
    _logwindow.clear()

class InputBox(object):

  def ask(self, prompt = ''):
    "Read input from the user, with optional prompt."
    _inputwindow.clear()
    _inputwindow.addstr(prompt, curses.A_BOLD)
    return _inputwindow.getstr(MAX_COLS - len(prompt)).decode()

message_log = MessageLog()
input_box = InputBox()
