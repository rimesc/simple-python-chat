from threading import Thread, Event

class Stoppable():

  def __init__(self):
    super(Stoppable, self).__init__()
    self.__stopped__ = Event()

  def is_stopped(self):
    return self.__stopped__.is_set()

  def stop(self):
    self.__stopped__.set()


class Listener(Stoppable, Thread):

  def __init__(self, reader, on_message):
    super(Listener, self).__init__()
    self._reader = reader
    self._on_message = on_message
    self.start()

  def run(self):
    while not self.is_stopped():
      self._reader.read(self._on_message)

  def stop(self):
    super(Listener, self).stop()
    self.join()
