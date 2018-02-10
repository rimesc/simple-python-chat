from chat import client
from time import sleep

# Actions
HELLO = 'HELLO'
SAY = 'SAY'
BYE = 'BYE'

# Keep track of who's online
people = {}

def message_received(ip, action, message):
  if action == HELLO:
    # someone new joined the conversation
    if not ip in people:
      name = message
      people[ip] = name
      print(name + ' joined the conversation')
      client.tell(ip, HELLO, my_name) # reply so that the new person knows who I am
  elif action == SAY:
    # someone said something
    name = people[ip] if ip in people else 'anonymous'
    print(name + ' said "' + message + '"')
  elif action == BYE:
    # someone has left the conversation
    if ip in people:
      name = people.pop(ip)
      print(name + ' left the conversation')

client = client()
client.when_message_received(message_received)
client.start_listening()
my_ip_address = client.ip_address
my_name = 'chris'
client.broadcast(HELLO, my_name)
client.broadcast(SAY, 'Hi!')
sleep(2)
client.broadcast(BYE)
client.stop_listening()