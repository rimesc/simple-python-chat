"""
Package providing a simple chat client.
"""
from socket import gethostbyname, gethostname
from .reader import Reader
from .writer import Writer
from .listener import Listener

class Client:
  """
  A simple chat client.

  Arguments:
  * port - network port to send and listen on
  """

  def __init__(self, port=50000):
    self.__reader = Reader(port)
    self.__writer = Writer(port)
    self.__listener = None

  def on_message_received(self, callback):
    """
    Set a function to be called when a new message arrives. The supplied function
    should accept 2 arguments: the address from which the message was sent (ip)
    and the content of the message (payload).
    """
    if self.__listener:
      self.__listener.stop()
    self.__listener = Listener(self.__reader, callback)

  def send_message(self, payload, ip = '<broadcast>'):
    """
    Send a message.  If an IP address is specified then the message will be sent to that
    address only; otherwise it will be broadcast to everyone on the network.
    """
    self.__writer.write(payload, ip)

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.__listener.stop()
    self.__reader.close()
    self.__writer.close()
