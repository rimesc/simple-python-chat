from chat import client
from terminal import run, new_window, read, write, NEW_LINE, BOLD

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
      write(log_window, name, style = BOLD)
      write(log_window, ' joined the conversation.', NEW_LINE)
      chat_client.tell(ip, HELLO, my_name) # reply so that the new person knows who I am
  elif action == SAY:
    # someone said something
    name = people[ip] if ip in people else 'anonymous'
    write(log_window, '[', name, '] ', style = BOLD)
    write(log_window, message, NEW_LINE)
  elif action == BYE:
    # someone has left the conversation
    if ip in people:
      name = people.pop(ip)
      write(log_window, name, style = BOLD)
      write(log_window, ' left the conversation.', NEW_LINE)
  write(input_window, '') # return focus to the input window

def main(screen_height, screen_width):
  global log_window, input_window
  # the chat log
  log_window = new_window(screen_height - 1, screen_width, 0, 0, scrolling = True)

  # the input for typing messages
  input_window = new_window(1, screen_width, screen_height-1, 0)

  chat_client.when_message_received(message_received)
  chat_client.start_listening()

  # let everyone know you're here
  chat_client.broadcast(HELLO, my_name)

  finished = False
  while not finished:
      input_window.clear()
      message = read(input_window, prompt = 'Write a message: ')
      if message.lower() == 'bye':
        finished = True
      else:
        chat_client.broadcast(SAY, message)

  chat_client.broadcast(BYE)
  chat_client.stop_listening()

run(main)

