from client import Client, MY_IP
import emoji
from terminal import Window, BOLD, NEW_LINE

# Actions
HELLO = 'HELLO'
SAY = 'SAY'
BYE = 'BYE'

# Keep track of who's online (ip address -> name)
people = {}

chat = Client(port = 50000)
window = Window()

# define a function to handle incoming messages
def handle_message(ip, action, message):
  if action == HELLO:
    # someone new joined the conversation
    if not ip in people:
      name = message
      people[ip] = name
      window.print(name, style = BOLD)
      window.print(' joined the conversation.', NEW_LINE)
      chat.tell(ip, HELLO, my_name) # reply so that the new person knows who I am
  elif action == SAY:
    # someone said something
    name = people[ip] if ip in people else 'anonymous'
    window.print('[', name, '] ', style = BOLD)
    window.print(message, NEW_LINE)
  elif action == BYE:
    # someone has left the conversation
    if ip in people:
      name = people.pop(ip)
      window.print(name, style = BOLD)
      window.print(' left the conversation.', NEW_LINE)

# call the function we defined whenever a new message arives
chat.on_message(handle_message)

# choose a user name
my_name = window.ask("What's your name? ")
people[MY_IP] = my_name

# let everyone know you're here
chat.broadcast(HELLO, my_name)

finished = False
while not finished:
    message = window.ask("Enter a message: ")
    # type 'bye' to leave the chat and exit the program
    if message.lower() == 'bye':
      finished = True
    else:
      message = emoji.replace(message)
      chat.broadcast(SAY, message)

# let everyone know you're leaving
chat.broadcast(BYE)
chat.close()
