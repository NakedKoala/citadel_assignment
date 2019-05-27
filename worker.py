from utils import *
import time, random
from threading import Thread
import asyncio

class Worker(Thread):
    def __init__(self, q, condition, n_event, analytics):
        Thread.__init__(self)
        self.n_event = n_event 
        self.q = q 
        self.condition =  condition
        self.verbose = True 
        self.analytics = analytics 
        self.loop_terminated = False
        self.proc_event = 0

        # Create event loop on a separate threaad
        self.loopWrapper = LoopWrapper(n_event, self)
        
    def set_verbose(self, val): 
        self.verbose = val 

    def compute_delay(self, event):
        return max(0, event.scheduled_time - time.time())

    def run(self):
        # Start the event loop on a separate thread
        self.loopWrapper.start()
        while not self.loop_terminated:
          self.condition.acquire()
          if self.proc_event < self.n_event:
            # Worker thread pause here until notified by the generator
            self.condition.wait()
          while len(self.q) > 0:
              # Pop events on the queue and schedule them with the event loop
              event = self.q.popleft()
              delay = self.compute_delay(event)
              # Register event with event loop 
              self.loopWrapper.loop.call_later(delay, self.loopWrapper.fire, event)
              self.proc_event += 1
          self.condition.release()


class LoopWrapper(Thread):
    def __init__(self, n_event, worker):
        Thread.__init__(self)
        self.loop = asyncio.new_event_loop()
        self.proc_event = 0 
        self.n_event = n_event
        self.worker = worker

    async def work(self, loop):
        while self.proc_event < self.n_event:
            # suspend  for a tiny time interval and allow
            # events to be fired
            await asyncio.sleep(0.0000000000000000000001)

    def fire(self, event):
        curr_time = time.time()
        #print fired event and record delta for computing summary statistic
        if self.worker.verbose:
            printGreen(f'FIRE -> Id: {event.id} | Scheduled Time: {format_time(event.scheduled_time)} | Fired Time: {format_time(curr_time)} |  delta { 1000 * abs(curr_time - event.scheduled_time) } MS')
        if self.worker.analytics != None:
            self.worker.analytics.add_delta(abs(curr_time - event.scheduled_time))

        self.proc_event += 1 

        # Terminate event loop when done
        if self.proc_event == self.n_event:
            for task in asyncio.Task.all_tasks():
                task.cancel()
            self.loop.stop()
            self.worker.loop_terminated = True

           

    def run(self):
        # start the event loop and run until all events are fired
        asyncio.set_event_loop(self.loop)
        self.loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.work(self.loop))
        self.loop.run_forever()
        