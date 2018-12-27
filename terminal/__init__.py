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
    """
    Print text to the message log.

    Arguments:
    * objects - objects to print
    * sep - string inserted between the objects (defaults to a single space)
    * end - string appended after the last object (defaults to a newline)
    * style - text style to use (BOLD|NORMAL; defaults to NORMAL)
    """
    for obj in objects[0:-1]:
      self.__print(obj, sep, style = style)
    self.__print(objects[-1], end, style = style)
    self.__input.addstr('') # return focus to the input window

  def __print(self, *objects, style):
    for obj in objects:
      self.__log.addstr(obj, style)

  def clear(self):
    """Clear the message log."""
    self.__log.clear()

  def ask(self, prompt = ''):
    """
    Read input from the user, with optional prompt.

    Arguments:
    * prompt - optional prompt text
    """
    self.__input.clear()
    self.__input.addstr(prompt, curses.A_BOLD)
    return self.__input.getstr(self.width - len(prompt)).decode()

