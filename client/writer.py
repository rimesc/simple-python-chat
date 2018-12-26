from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from .common import MAGIC_NUMBER

class _Writer:

  def __init__(self, port):
    self.port = port
    self._socket = socket(AF_INET, SOCK_DGRAM) # create UDP socket
    self._socket.bind(('', 0))
    self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) # this is a broadcast socket

  def write(self, action, payload, ip='<broadcast>'):
    "Send a message to the given address (if ip is omitted, broadcast to everyone)."
    data = '%s:%s:%s' % (MAGIC_NUMBER, action, payload)
    self._socket.sendto(data.encode(), (ip, self.port))

  def close(self):
    self._socket.close()
