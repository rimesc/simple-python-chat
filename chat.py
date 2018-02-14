"""
A simple chat client.

Functions:
* client() - create a new client
"""
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname, timeout
from util import forever

DEFAULT_PORT = 50000
MAGIC_NUMBER = "fna349fn" #to make sure we don't confuse or get confused by other programs

class Client:
  """
  Simple chat client.

  Operations:
  * when_message_received(callback) - set a function to be called when a new message arrives
  * start_listening() - start listening for messages
  * stop_listening() - stop listening for messages
  * broadcast(action, message) - send a message to everyone
  * tell(ip, action, message) - send a message to one person

  The callback function passed to when_message_received should accept 3 arguments:
  * ip - the address from which the message was sent
  * action - the action (e.g. 'HELLO', 'SAY', 'BYE')
  * message - the content of the message
  """

  def __init__(self, port=DEFAULT_PORT):
    self.port = port
    self.ip_address = gethostbyname(gethostname()) # get our IP. Be careful if you have multiple network interfaces or IPs
    self.__read_socket = socket(AF_INET, SOCK_DGRAM)
    self.__read_socket.bind(('', self.port))
    self.__read_socket.settimeout(1.0)
    self.__write_socket = socket(AF_INET, SOCK_DGRAM) #create UDP socket
    self.__write_socket.bind(('', 0))
    self.__write_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket
    self.__listener = forever(self.__listen)

  def start_listening(self):
    "Start listening for new messages."
    self.__listener.start()

  def stop_listening(self):
    "Stop listening for new messages."
    self.__listener.stop()
    self.__listener.join()
  
  def when_message_received(self, callback):
    "Set a function that will be called for each new message received."
    self.__onmessage = callback

  def broadcast(self, action, payload=''):
    "Broadcast a message to everyone on the network."
    self.__send(action, payload)

  def tell(self, ip, action, payload=''):
    "Send a message to a single person."
    self.__send(action, payload, ip)

  def __send(self, action, payload, ip='<broadcast>'):
    data = '%s:%s:%s' % (MAGIC_NUMBER, action, payload)
    self.__write_socket.sendto(data.encode(), (ip, self.port))

  def __listen(self):
    try:
      (ip, data) = self.__read()
      if data.startswith(MAGIC_NUMBER):
        (_, action, payload) = data.split(':')
        self.__onmessage(ip, action, payload)
    except timeout:
        pass

  def __read(self):
    data, (ip, _) = self.__read_socket.recvfrom(1024) # wait for a packet
    return (ip, data.decode())

client = Client
