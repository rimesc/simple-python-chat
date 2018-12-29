from socket import socket, AF_INET, SOCK_DGRAM, timeout
from .common import MAGIC_NUMBER

class Reader:

  def __init__(self, port, timeout=1.0):
    self._socket = socket(AF_INET, SOCK_DGRAM)
    self._socket.bind(('', port))
    self._socket.settimeout(timeout)

  def read(self, on_message):
    try:
      (ip, data) = self._receive()
      if data.startswith(MAGIC_NUMBER):
        (_, payload) = data.split(':', maxsplit=1)
        on_message(ip, payload)
    except timeout:
        pass

  def close(self):
    self._socket.close()

  def _receive(self):
    data, (ip, _) = self._socket.recvfrom(1024) # wait for a packet
    return (ip, data.decode())
