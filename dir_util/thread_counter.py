from dir_util.util import Util
import _thread
from machine import Pin

class Thread_Counter:
    def __init__(self, buzzer_pin):
        self._running           = False
        self._allow_running     = False
        self._counter           = None
        self._counter_limit     = None
        self._beep_per_second   = None
        self._buzzer            = Pin(buzzer_pin, Pin.OUT)
        self._buzzer.value(0)
       
    def start_counter(self, counter_limit):
        if(self._allow_running):
            self._allow_running = False
        
        self.wait_terminate()
        self.set_vars_counter(counter_limit)
    
        self._my_thread  = _thread.start_new_thread(self.contar, ())
    
    def start_beep(self, beep_per_second):
        if(self._allow_running):
            self._allow_running = False
        
        self.wait_terminate()
        self.set_vars_beep(beep_per_second)
        
        self._my_thread       = _thread.start_new_thread(self.beep, ())
        
    def contar(self):
        while(self._counter > 0 and self._allow_running):
            Util.wait_sec(1)
            self._counter -= 1
        self.set_control_variables(False)
    
    def beep(self):
        aux_calc = int(1000/self._beep_per_second)
        print("AQUI: ", self._allow_running)
        while(self._allow_running):
            Util.wait_ms(aux_calc)
            self.buzzer_change_state()

        self.set_control_variables(False)
    
    def set_vars_counter(self, counter_limit):
        self._buzzer.value(0)
        self._beep_per_second = None
        self._counter_limit   = counter_limit
        self._counter         = counter_limit
        self.set_control_variables(True)

    def set_vars_beep(self, beep_per_second):
        self._buzzer.value(0)
        self._beep_per_second = beep_per_second
        self._counter_limit   = None
        self._counter         = None
        self.set_control_variables(True)
    
    def buzzer_change_state(self):
        if self._buzzer.value() == 1:
            self._buzzer.value(0)
        else:
            self._buzzer.value(1)
    
    def wait_terminate(self):
        while self._running == True: 
            Util.wait_ms(10)

    def stop(self):
        self._allow_running = False
        self._buzzer.value(0)
        self.wait_terminate()
    
    def reset(self):
        if self.check_thread():
            self.stop()
            self._running           = False
            self._allow_running     = False
            self._counter           = None
            self._counter_limit     = None
            self._beep_per_second   = None
    
    def set_control_variables(self, state):
        self._allow_running = state
        self._running = state
    
    def check_thread_counter(self):
        return self._counter_limit != None

    def check_thread_beep(self):
        return self._beep_per_second != None
    
    def check_thread(self):
        return self._counter_limit != None or self._beep_per_second != None
    
    def is_running(self):
        return self._running

    def get_counter_limit(self):
        return self._counter_limit    
    
    def get_counter(self):
        return self._counter 