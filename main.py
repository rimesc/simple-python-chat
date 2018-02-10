import curses
from chat import client
from curses import newwin, A_BOLD
from curses_extra import run
from time import sleep

# Actions
HELLO = 'HELLO'
SAY = 'SAY'
BYE = 'BYE'

my_name = 'chris'
chat_client = client()

# Keep track of who's online (ip address -> name)
people = {chat_client.ip_address: my_name}

def message_received(ip, action, message):
  if action == HELLO:
    # someone new joined the conversation
    if not ip in people:
      name = message
      people[ip] = name
      log_window.addstr(name, A_BOLD)
      log_window.addstr(' joined the conversation.\n')
      chat_client.tell(ip, HELLO, my_name) # reply so that the new person knows who I am
  elif action == SAY:
    # someone said something
    name = people[ip] if ip in people else 'anonymous'
    log_window.addstr('[' + name + '] ', A_BOLD)
    log_window.addstr(message + '\n')
  elif action == BYE:
    # someone has left the conversation
    if ip in people:
      name = people.pop(ip)
      log_window.addstr(name, A_BOLD)
      log_window.addstr(' left the conversation.\n')

def main(screen_height, screen_width):
  global log_window, input_window
  # set up the chat log
  log_window = newwin(screen_height - 2, screen_width, 0, 0)
  log_window.scrollok(True)  # when the window is full, scroll old messages off the top
  log_window.immedok(True)  # update immediately when a new message arrives

  # set up the input for typing messages
  input_window = newwin(2, screen_width, screen_height-2, 0)
  input_window.hline(curses.ACS_HLINE, screen_width)
  input_window.addstr(0, 0, 'Write a message: ')
  input_window.refresh()

  chat_client.when_message_received(message_received)
  chat_client.start_listening()

  # let everyone know you're here
  chat_client.broadcast(HELLO, my_name)

  finished = False
  while not finished:
      input_window.move(1, 0)
      input_window.clrtoeol()  # clear the input area ready for a new message
      message = input_window.getstr(screen_width).decode()
      if message.lower() == 'bye':
        finished = True
      else:
        chat_client.broadcast(SAY, message)

  chat_client.broadcast(BYE)
  chat_client.stop_listening()

run(main)

