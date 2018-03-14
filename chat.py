import client as chat
from terminal import new_window, SCREEN_HEIGHT, SCREEN_WIDTH, NEW_LINE, BOLD

# Actions
HELLO = 'HELLO'
SAY = 'SAY'
BYE = 'BYE'

my_name = 'alice'

# Keep track of who's online (ip address -> name)
people = {chat.ip_address: my_name}

# divide the window into a scrolling chat log and an input box for typing messages
log_window = new_window(SCREEN_HEIGHT - 1, SCREEN_WIDTH, 0, 0, scrolling = True)
input_window = new_window(1, SCREEN_WIDTH, SCREEN_HEIGHT - 1, 0)

# define a function to handle incoming messages
def message_received(ip, action, message):
  if action == HELLO:
    # someone new joined the conversation
    if not ip in people:
      name = message
      people[ip] = name
      log_window.write(name, style = BOLD)
      log_window.write(' joined the conversation.', NEW_LINE)
      chat.tell(ip, HELLO, my_name) # reply so that the new person knows who I am
  elif action == SAY:
    # someone said something
    name = people[ip] if ip in people else 'anonymous'
    log_window.write('[', name, '] ', style = BOLD)
    log_window.write(message, NEW_LINE)
  elif action == BYE:
    # someone has left the conversation
    if ip in people:
      name = people.pop(ip)
      log_window.write(name, style = BOLD)
      log_window.write(' left the conversation.', NEW_LINE)
  input_window.write('') # return focus to the input window

chat.when_message_received(message_received)

# let everyone know you're here
chat.broadcast(HELLO, my_name)

finished = False
while not finished:
    input_window.clear()
    message = input_window.read(prompt = 'Write a message: ')
    if message.lower() == 'bye':
      finished = True
    else:
      chat.broadcast(SAY, message)

chat.broadcast(BYE)
chat.stop()
