from socket import socket, AF_INET, SOCK_DGRAM, timeout
from .common import MAGIC_NUMBER

class Reader:

  def __init__(self, port, timeout=1.0):
    self.__socket = socket(AF_INET, SOCK_DGRAM)
    self.__socket.bind(('', port))
    self.__socket.settimeout(timeout)

  def read(self, on_message):
    try:
      (ip, data) = self.__receive()
      if data.startswith(MAGIC_NUMBER):
        (_, payload) = data.split(':', maxsplit=1)
        on_message(ip, payload)
    except timeout:
        pass

  def close(self):
    self.__socket.close()

  def __receive(self):
    data, (ip, _) = self.__socket.recvfrom(1024) # wait for a packet
    return (ip, data.decode())
