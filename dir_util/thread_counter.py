from dir_util.util import Util
import _thread

class Thread_Counter:
    def __init__(self, counter_limit):
        self._running       = True
        self._counter       = counter_limit
        self._counter_limit = counter_limit
        self._my_thread     = _thread.start_new_thread(self.contar, ())

    def contar(self):
        while(self._counter > 0 and self._running):
            Util.wait_sec(1)
            self._counter -= 1
        self._running = False
    
    def is_running(self):
        return self._running

    def get_counter(self):
        return self._counter
    
    def set_running(self, status):
        self._running = status

# from concurrent.futures import ThreadPoolExecutor

# class Thread_Counter:
#     def __init__(self, counter_limit):
#         self._running = True
#         self._counter = counter_limit
#         self._counter_limit = counter_limit
#         self._executor = ThreadPoolExecutor(max_workers=2)
#         self._future = self._executor.submit(self.contar)

#     def contar(self):
#         while self._counter > 0 and self._running:
#             Util.wait_sec(1)
#             self._counter -= 1
#         self._running = False

#     def is_running(self):
#         return self._running

#     def get_counter(self):
#         return self._counter

#     def set_running(self, status):
#         self._running = status
