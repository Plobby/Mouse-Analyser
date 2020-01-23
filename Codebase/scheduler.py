import time
from threading import Event, Thread

class Scheduler(Thread):
    # Constructor
    def __init__(self, interval, function):
        # Configure thread settings
        Thread.__init__(self)
        self.setDaemon(True)

        self.interval = interval
        self.function = function
        self.start_time = time.time()
        self.event = Event()
    
    def run(self):
        while (not self.event.wait(self._time)):
            self.function()

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start_time) % self.interval)

    def stop(self):
        self.event.set()
        self.join()