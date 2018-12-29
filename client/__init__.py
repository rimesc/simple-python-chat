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

  Arguments:
  * port - network port to send and listen on
  """

  def __init__(self, port=50000):
    self._reader = Reader(port)
    self._writer = _Writer(port)
    self._listener = None

  def on_message_received(self, callback):
    """
    Set a function to be called when a new message arrives. The supplied function
    should accept 2 arguments: the address from which the message was sent (ip)
    and the content of the message (payload).
    """
    if self._listener:
      self._listener.stop()
    self._listener = Listener(self._reader, callback)

  def send_message(self, payload, ip = '<broadcast>'):
    """
    Send a message.  If an IP address is specified then the message will be sent to that
    address only; otherwise it will be broadcast to everyone on the network.
    """
    self._writer.write(payload, ip)

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self._listener.stop()
    self._reader.close()
    self._writer.close()
