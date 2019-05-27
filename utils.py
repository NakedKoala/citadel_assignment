import datetime
class TimeEvent:
    def __init__(self, id, curr_time, delay):
        self.id, self.curr_time, self.delay = id, curr_time, delay
        self.scheduled_time = curr_time + delay 
    def __repr__(self):
        return f'id: {self.id} | curr_time: {format_time(self.curr_time)} | scheduled_time: {format_time(self.scheduled_time)} | random_delay: {self.delay * 1000 } MS'


def printRed(skk): 
    print("\033[91m {}\033[00m" .format(skk)) 
def printGreen(skk): 
    print("\033[92m {}\033[00m" .format(skk)) 
def format_time(t): 
    return datetime.datetime.utcfromtimestamp(t).time()

class Analytics:
    '''
    Compute summary statistic for delta over large number of events
    Require numpy as dependency
    '''
    def __init__(self):
        self.delta = []
        self.size = 0

    def add_delta(self, delta):
        self.delta[self.size] = delta
        self.size += 1

    def run(self, test, n_event):
        self.delta = [None] * n_event
        print(f'Running {n_event} events for summary statistic')
        test(n_event, False, self)
        self.print_summary(n_event)

    def print_summary(self, n_event):
        import numpy as np 
        self.delta = np.array(self.delta)
        average = np.mean(self.delta)
        std = np.std(self.delta)
        print("########################################")
        print(f'Summary Statistic for {n_event} events ')
        print("")
        
        print(f'Average delta per event: {average * 1000} MS')  
        print(f'Median {np.percentile(self.delta, 50 ) * 1000} MS')
        print(f'Standard deviation: {std} MS')
        print("########################################")
       
        
