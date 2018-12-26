"""
Utilities for working with the terminal.

Splits the terminal into two parts - a scrolling message log and a user input
box - and provides facades for accessing the two parts.

Constants:
* NORMAL - style constant used with the write function to produce normal text
* BOLD - style constant used with the write function to produce bold text

Classes:
* Window - the chat window
"""
import curses

BOLD = curses.A_BOLD
NORMAL = curses.A_NORMAL

class Window:
  """
  Divides the terminal into two parts - a scrolling message log and a user input
  box - and provides methods for accessing the two parts.

  Members:
  * print(value, ..., style) - write to the message log
  * clear() - clear the message log
  * ask(prompt) - prompt the user for input
  * height - height in lines of the terminal window
  * width - width in characters of the terminal window
  """

  height = curses.LINES  # pylint: disable=no-member
  width = curses.COLS    # pylint: disable=no-member

  def __init__(self):
    super(Window, self).__init__()
    self.__main = curses.newwin(self.height, self.width, 0, 0)
    self.__main.immedok(True)  # update immediately
    self.__main.hline(self.height - 2, 0, curses.ACS_HLINE, self.width)
    # divide the main window into a scrolling chat log and an input box for typing messages
    self.__log = self.__main.subwin(self.height - 2, self.width, 0, 0)
    self.__log.immedok(True)  # update immediately
    self.__log.scrollok(True)
    self.__input = self.__main.subwin(1, self.width, self.height - 1, 0)
    self.__input.immedok(True)  # update immediately

  def print(self, *objects, sep = ' ', end = '\n', style = NORMAL):
    "Write text starting at the current position of the cursor."
    for obj in objects:
      self.__log.addstr(obj, style)
      self.__log.addstr(sep, style)
    self.__log.addstr(end, style)
    self.__input.addstr('') # return focus to the input window

  def clear(self):
    self.__log.clear()

  def ask(self, prompt = ''):
    "Read input from the user, with optional prompt."
    self.__input.clear()
    self.__input.addstr(prompt, curses.A_BOLD)
    return self.__input.getstr(self.width - len(prompt)).decode()

