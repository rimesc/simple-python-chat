from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname, timeout
from time import sleep, time
from util import forever

MAGIC_NUMBER = "fna349fn" #to make sure we don't confuse or get confused by other programs

SAY = 'SAY'
JOIN = 'JOIN'
GREET = 'GREET'
LEAVE = 'LEAVE'

class Client:

  def __init__(self, port=50000):
    self.__port = port
    self.__read_socket = socket(AF_INET, SOCK_DGRAM)
    self.__read_socket.bind(('', self.__port))
    self.__read_socket.settimeout(1.0)
    self.__write_socket = socket(AF_INET, SOCK_DGRAM) #create UDP socket
    self.__write_socket.bind(('', 0))
    self.__write_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket
    self.__my_ip = gethostbyname(gethostname()) #get our IP. Be careful if you have multiple network interfaces or IPs
    self.__people = {}

  def join(self, name):
    self.__people[self.__my_ip] = name
    self.__listen()
    self.__send(JOIN, name)
  
  def leave(self):
    if (self.__thread):
      self.__thread.stop()
    self.__send(LEAVE)
  
  def say(self, message):
    self.__send(SAY, message)

  def when_message_received(self, callback):
    self.__onmessage = callback

  def when_someone_joins(self, callback):
    self.__onjoin = callback

  def when_someone_leaves(self, callback):
    self.__onleave = callback

  def __send(self, action, payload = ''):
    data = '%s:%s:%s' % (MAGIC_NUMBER, action, payload)
    self.__write_socket.sendto(data.encode(), ('<broadcast>', self.__port))

  def __listen(self):
    self.__thread = forever(self.__poll_for_messages)

  def __poll_for_messages(self):
    try:
      data, (ip, _) = self.__read_socket.recvfrom(1024) #wait for a packet
      if data.decode().startswith(MAGIC_NUMBER):
          (_, action, payload) = data.decode().split(':')
          if action == GREET:
            if not ip in self.__people:
              self.__people[ip] = payload
              self.__onjoin(payload)
          elif action == JOIN:
            if not ip in self.__people:
              self.__people[ip] = payload
              self.__onjoin(payload)
              self.__send(GREET, self.__people[self.__my_ip])
          elif action == SAY:
            if ip in self.__people:
              self.__onmessage(self.__people[ip], payload)
          elif action == LEAVE:
            if ip in self.__people:
              name = self.__people.pop(ip)
              self.__onleave(name)
    except timeout:
        pass

client = Client

def new_member_joined(name):
  print(name + ' joined')

def member_left(name):
  print(name + ' left')

def print_message(name, message):
  print(name + ' said ' + message)

client = client()
client.when_someone_joins(new_member_joined)
client.when_message_received(print_message)
client.when_someone_leaves(member_left)
client.join('me')
client.say('Hi!')
sleep(2)
client.leave()