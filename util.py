from threading import Thread, Event

class StoppableThread(Thread):

  def __init__(self, target):
    super(StoppableThread, self).__init__()
    self.__target = target
    self.__stop = Event()

  def run(self):
    while not self.__stop.is_set():
      self.__target()

  def start(self):
    self.__stop.clear()
    super(StoppableThread, self).start()

  def stop(self):
    self.__stop.set()

forever = StoppableThread

