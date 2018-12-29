from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from .common import MAGIC_NUMBER

class Writer:

  def __init__(self, port):
    self.__port = port
    self.__socket = socket(AF_INET, SOCK_DGRAM) # create UDP socket
    self.__socket.bind(('', 0))
    self.__socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) # this is a broadcast socket

  def write(self, payload, ip='<broadcast>'):
    data = '%s:%s' % (MAGIC_NUMBER, payload)
    self.__socket.sendto(data.encode(), (ip, self.__port))

  def close(self):
    self.__socket.close()
