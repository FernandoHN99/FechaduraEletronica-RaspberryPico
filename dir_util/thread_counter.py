from dir_util.util import Util
import _thread

class Thread_Counter:
    def __init__(self, counter_limit):
        self._running       = True
        self._counter_limit = counter_limit
        self.my_thread      = _thread.start_new_thread(self.contar, ())

    def contar(self):
        counter = 0
        while(counter < self._counter_limit):
            Util.wait_sec(1)
            counter += 1
        self._running = False
    
    def get_running(self):
        return self._running

if __name__ == '__main__':
    t1 = Thread_Counter(5)
    while(t1.get_running()):
        print(t1.get_running())
        print("Rodando")
    print("fim")
