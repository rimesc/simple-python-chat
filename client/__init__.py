"""
Package providing a simple chat client.

Constants:
* MY_IP - IP address of this computer

Classes:
* Client - a chat client
"""
from socket import gethostbyname, gethostname
from .reader import Reader
from .writer import _Writer
from .listener import Listener

MY_IP = gethostbyname(gethostname()) # get our IP. Be careful if you have multiple network interfaces or IPs

class Client:
  """
  A simple chat client.

  Operations:
  * on_message(callback) - set a function to be called when a new message arrives
  * broadcast(action, message) - send a message to everyone
  * tell(ip, action, message) - send a message to one person
  * stop() - stop listening for messages

  Arguments:
  * port - network port to send and listen on

  The callback function passed to on_message should accept 3 arguments:
  * ip - the address from which the message was sent
  * action - the action (e.g. 'HELLO', 'SAY', 'BYE')
  * message - the content of the message
  """

  def __init__(self, port=50000):
    self._reader = Reader(port)
    self._writer = _Writer(port)
    self._listener = None

  def on_message(self, callback):
    "Set a function to be called when a new message arrives."
    if self._listener:
      self._listener.stop()
    self._listener = Listener(self._reader, callback)

  def broadcast(self, action, payload=''):
    "Broadcast a message to everyone on the network."
    self._writer.write(action, payload)

  def tell(self, ip, action, payload=''):
    "Send a message to a single person."
    self._writer.write(action, payload, ip)

  def close(self):
    "Stop listening for new messages."
    self._listener.stop()
    self._reader.close()
    self._writer.close()