from dir_util.util import Util
import threading

class Thread_Counter:
    def __init__(self, counter_limit):
        self._running = True
        self._counter_limit = counter_limit
        self._thread = threading.Thread(target=self.contar)
        self._thread.start()

    def contar(self):
        counter = 0
        while(counter < self._counter_limit):
            Util.wait_sec(1)
            counter += 1
        self._running = False
    
    def get_running(self):
        return self._running

