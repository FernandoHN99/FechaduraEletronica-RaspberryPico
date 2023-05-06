from dir_util.util import Util
import _thread

class Thread_Counter:
    def __init__(self):
        self._running           = False
        self._allow_running     = False
        self._counter           = None
        self._counter_limit     = None
       
    def start(self, counter_limit):
        if(self._allow_running):
            self._allow_running = False

        while self._running == True: 
            Util.wait_ms(10)
            print("self._running: ", self._running)

        print("Iniciei a nova thread")
        self._my_thread  = _thread.start_new_thread(self.contar, (counter_limit,))
    
    def stop(self):
        self._allow_running = False

    def set_variables_on(self, counter_limit):
        self.set_control_variables(True)
        self._counter       = counter_limit
        self._counter_limit = counter_limit
    
    def set_control_variables(self, state):
        self._allow_running = state
        self._running = state

    def contar(self, counter_limit):
        self.set_variables_on(counter_limit) 
        while(self._counter > 0 and self._allow_running):
            Util.wait_sec(1)
            self._counter -= 1
        self.set_control_variables(False)
        print("Parei a Thread")

    
    def is_running(self):
        return self._running

    def get_counter_limit(self):
        return self._counter_limit    
    
t1 = Thread_Counter()
t1.start(2)
Util.wait_ms(1)
t1.start(2)
Util.wait_ms(1)
t1.start(2)



