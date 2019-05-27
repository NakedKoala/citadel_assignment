from collections import deque 
from threading import Condition
from utils import * 
import gc 
from generator import * 
from worker import * 

def test(n_event, verbose, analytics = None):
    # Testing the program on n events


    # init Q and condition shared by the worker and generator
    q = deque()
    condition = Condition()

    # Init generator and worker
    my_generator = Generator(q, condition, n_event)
    my_generator.set_verbose(verbose)
    my_worker =  Worker(q, condition, n_event, analytics)
    my_worker.set_verbose(verbose)
    
    # start them on separate threads
    my_generator.start()
    my_worker.start()

    my_generator.join()
    my_worker.join() 


if __name__ == "__main__":
    gc.disable()
    # Test 20 events with print out
    test(n_event = 20, verbose = True, analytics = None)

    # To test unlimited number of event pass float('inf') as first paraamt
    
    # test(float('inf'), True, None)

    # Uncomment to see summary statistic if
    # you have numpy installed 

    # analytics = Analytics()
    # analytics.run(test, 50)