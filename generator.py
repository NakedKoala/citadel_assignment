from utils import *
import time, random
from threading import Thread

class Generator(Thread):
  def __init__(self, q, condition, n_event):

    Thread.__init__(self)
    self.n_event = n_event
    self.condition = condition
    self.generated_event = 0 
    self.q = q 
    self.verbose = True 
    
  def set_verbose(self, val): 
      self.verbose = val 

  def run(self):
      while self.generated_event < self.n_event:
          time.sleep(0.1)
          # Generate event
          delay = float(random.randint(0, 200)) / float(1000)
          event = TimeEvent(self.generated_event, time.time(), delay)
          self.generated_event += 1 

          # Append to threadsafe queue and notify worker via self.condition
          self.condition.acquire()
          self.q.append(event)
          if self.verbose:
            printRed(f'GENERATE -> {event}')
          self.condition.notify()
          self.condition.release()