
## How to run

  

To test the program, run test.py file with python 3.7.3 or above.
The main program has no external dependency, but the analytics class requires numpy.

  
  



  

## Performance metrics (calculated by running 500 events on my local machine )


* Average delta between scheduled & fire time: 0.26 milliseconds.

* Standard deviation of the delta: 0.0041 milliseconds.

  
  
## Implementation Summary

* Producer & Consumer model via synchronized queue and condition variable

  

	The Generator thread awakens the worker thread after adding an event to the queue. The worker thread then registers the event with the event loop ( explained below ). The worker thread then suspends and releases the lock waiting for the next notification from the generator thread.

  
  

* Single-threaded concurrent task scheduler using Asyncio library

  

	Asyncio: Asyncio simulates single-threaded concurrency by suspending execution of code blocks (for tiny time intervals )and yield the execution to other code block. Suspension of current code block is achieved through "await" syntax

  

	Event Loop: Event loop is used as a scheduler for registering asynchronous task. It runs on its own thread. The execution time of the registered event is close to the scheduled time due to the concurrency made possible by the mechanism described above. When the worker thread pulls a task from the queue, it registers the task with the event loop immediately.