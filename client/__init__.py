"""
Package providing a simple chat client.
"""
from socket import gethostbyname, gethostname
from .reader import Reader
from .writer import _Writer
from .listener import Listener

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

  def on_message_received(self, callback):
    "Set a function to be called when a new message arrives."
    if self._listener:
      self._listener.stop()
    self._listener = Listener(self._reader, callback)

  def send_message(self, payload, ip = '<broadcast>'):
    """
    Send a message.  If an IP address is specified then the message will be sent to that
    address; otherwise it will be broadcast to everyone on the network.
    """
    self._writer.write(payload, ip)

  def close(self):
    "Stop listening for new messages."
    self._listener.stop()
    self._reader.close()
    self._writer.close()
