"""
A simple chat client.

Constants:
* my_ip - IP address of this computer

Functions:
* client(port, on_message) - create a new chat client, with optional port and an optional
                             function to be called when a new message arrives
"""
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname, timeout
from threading import Thread, Event

_MAGIC_NUMBER = "fna349fn" # to make sure we don't confuse or get confused by other programs

my_ip = gethostbyname(gethostname()) # get our IP. Be careful if you have multiple network interfaces or IPs

class client:
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
    self._reader = _Reader(port)
    self._writer = _Writer(port)
    self._listener = None

  def on_message(self, callback):
    "Set a function to be called when a new message arrives."
    if self._listener:
      self._listener.stop()
    self._listener = _Listener(self._reader, callback)

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


class _Reader:

  def __init__(self, port, timeout=1.0):
    self._socket = socket(AF_INET, SOCK_DGRAM)
    self._socket.bind(('', port))
    self._socket.settimeout(timeout)

  def read(self, on_message):
    "Wait a short time for a message to be received and invoke the callback if one arrives."
    try:
      (ip, data) = self._receive()
      if data.startswith(_MAGIC_NUMBER):
        (_, action, payload) = data.split(':', maxsplit=2)
        on_message(ip, action, payload)
    except timeout:
        pass

  def close(self):
    self._socket.close()

  def _receive(self):
    data, (ip, _) = self._socket.recvfrom(1024) # wait for a packet
    return (ip, data.decode())

  
class _Writer:

  def __init__(self, port):
    self.port = port
    self._socket = socket(AF_INET, SOCK_DGRAM) # create UDP socket
    self._socket.bind(('', 0))
    self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) # this is a broadcast socket

  def write(self, action, payload, ip='<broadcast>'):
    "Send a message to the given address (if ip is omitted, broadcast to everyone)."
    data = '%s:%s:%s' % (_MAGIC_NUMBER, action, payload)
    self._socket.sendto(data.encode(), (ip, self.port))

  def close(self):
    self._socket.close()


class _Stoppable():

  def __init__(self):
    self.__stopped__ = Event()

  def is_stopped(self):
    return self.__stopped__.is_set()

  def stop(self):
    self.__stopped__.set()


class _Listener(Thread, _Stoppable):

  def __init__(self, reader, on_message):
    super(_Listener, self).__init__()
    self._reader = reader
    self._on_message = on_message
    self.start()

  def run(self):
    while not self.is_stopped():
      self._reader.read(self._on_message)

  def stop(self):
    super(_Listener, self).stop()
    self.join()
