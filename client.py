"""
A simple chat client.

Functions:
* when_message_received(callback) - set a function to be called when a new message arrives
* broadcast(action, message) - send a message to everyone
* tell(ip, action, message) - send a message to one person
* stop() - stop listening for messages

Constants:
* ip_address - IP address of this computer

The callback function passed to when_message_received should accept 3 arguments:
* ip - the address from which the message was sent
* action - the action (e.g. 'HELLO', 'SAY', 'BYE')
* message - the content of the message
"""
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname, timeout
from threading import Thread, Event

ip_address = gethostbyname(gethostname()) # get our IP. Be careful if you have multiple network interfaces or IPs

def broadcast(action, payload=''):
  "Broadcast a message to everyone on the network."
  _client.send(action, payload)

def tell(ip, action, payload=''):
  "Send a message to a single person."
  _client.send(action, payload, ip)

def stop():
  "Stop listening for new messages."
  _listener.stop()

def when_message_received(callback):
  "Set a function that will be called for each new message received."
  global _listener
  if (_listener):
    _listener.stop()
  _listener = Listener(callback)

class Client:
  """
  Simple chat client.

  Operations:
  * send(action, payload[, ip]) - send a message to the given address (if ip is omitted, broadcast to everyone)
  * receive(callback) - wait a short time for a message to be received and invoke the callback if one arrives
  """

  def __init__(self, port=50000):
    self.port = port
    self.__read_socket = socket(AF_INET, SOCK_DGRAM)
    self.__read_socket.bind(('', self.port))
    self.__read_socket.settimeout(1.0)
    self.__write_socket = socket(AF_INET, SOCK_DGRAM) #create UDP socket
    self.__write_socket.bind(('', 0))
    self.__write_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket
    self.__magic_number = "fna349fn" # to make sure we don't confuse or get confused by other programs

  def send(self, action, payload, ip='<broadcast>'):
    data = '%s:%s:%s' % (self.__magic_number, action, payload)
    self.__write_socket.sendto(data.encode(), (ip, self.port))

  def receive(self, callback):
    try:
      (ip, data) = self.__read()
      if data.startswith(self.__magic_number):
        (_, action, payload) = data.split(':')
        callback(ip, action, payload)
    except timeout:
        pass

  def __read(self):
    data, (ip, _) = self.__read_socket.recvfrom(1024) # wait for a packet
    return (ip, data.decode())


class Listener(Thread):
  "A listener that polls the client for messages and invokes the callback for each one."
  def __init__(self, callback):
    super(Listener, self).__init__()
    self.__callback = callback
    self.__stopped = Event()
    self.start()

  def run(self):
    while not self.is_stopped():
      _client.receive(self.__callback)

  def is_stopped(self):
    return self.__stopped.is_set()

  def stop(self):
    self.__stopped.set()
    self.join()


_client = Client()

_listener = None