import client as chat
from terminal import message_log, input_box, BOLD, NEW_LINE

# Actions
HELLO = 'HELLO'
SAY = 'SAY'
BYE = 'BYE'

# Keep track of who's online (ip address -> name)
people = {}

# define a function to handle incoming messages
def message_received(ip, action, message):
  if action == HELLO:
    # someone new joined the conversation
    if not ip in people:
      name = message
      people[ip] = name
      message_log.print(name, style = BOLD)
      message_log.print(' joined the conversation.', NEW_LINE)
      chat.tell(ip, HELLO, my_name) # reply so that the new person knows who I am
  elif action == SAY:
    # someone said something
    name = people[ip] if ip in people else 'anonymous'
    message_log.print('[', name, '] ', style = BOLD)
    message_log.print(message, NEW_LINE)
  elif action == BYE:
    # someone has left the conversation
    if ip in people:
      name = people.pop(ip)
      message_log.print(name, style = BOLD)
      message_log.print(' left the conversation.', NEW_LINE)

chat.when_message_received(message_received)

my_name = input_box.ask("What's your name? ")
my_ip = chat.ip_address
people[my_ip] = my_name

# let everyone know you're here
chat.broadcast(HELLO, my_name)

finished = False
while not finished:
    message = input_box.ask("Enter a message: ")
    if message.lower() == 'bye':
      finished = True
    else:
      chat.broadcast(SAY, message)

chat.broadcast(BYE)
chat.stop()
