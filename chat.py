from client import Client, MY_IP
import emoji
from terminal import Window, BOLD

# actions
HELLO = 'HELLO'
SAY = 'SAY'
BYE = 'BYE'

# create the chat window
window = Window()

# choose a user name
my_name = window.ask("What's your name? ")

# keep track of who's online (ip address -> name)
people = {}

# define a function to handle incoming messages
def handle_message(ip, payload):
  (action, message) = decode(payload)
  if action == HELLO:
    # someone new joined the conversation
    if not ip in people:
      name = message
      people[ip] = name
      window.print(name, 'joined the conversation.', style = BOLD)
      chat.send_message(encode(HELLO, my_name), ip = ip) # reply so that the new person knows who I am
  elif action == SAY:
    # someone said something
    name = people[ip] if ip in people else 'anonymous'
    colour = (13 * int(ip.split('.')[3])) % window.colors
    window.print('[', name, ']', style = BOLD, colour = colour, end=' ', sep = '')
    window.print(message, colour = colour)
  elif action == BYE:
    # someone has left the conversation
    if ip in people:
      name = people.pop(ip)
      window.print(name, 'left the conversation.', style = BOLD)

# decode an incoming message
def decode(payload):
  return payload.split(':', maxsplit=1)

# encode an outgoing message
def encode(action, message):
  return '%s:%s' % (action, message)

# create the chat client
chat = Client(port = 50000)

# call the function we defined whenever a new message arrives
chat.on_message_received(handle_message)

# let everyone know you're here
chat.send_message(encode(HELLO, my_name))

finished = False
while not finished:
    message = window.ask("Enter a message: ")
    # type 'bye' to leave the chat and exit the program
    if message.lower() == 'bye':
      finished = True
    else:
      message = emoji.replace(message)
      chat.send_message(encode(SAY, message))

# let everyone know you're leaving
chat.send_message(BYE)
chat.close()
