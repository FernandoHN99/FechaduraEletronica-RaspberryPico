from dir_util.util import Util
import _thread
from machine import Pin

class Thread:
    def __init__(self, buzzer_pin):
        self._running               = False
        self._control_running       = False
        self._current_process       = None
        self._completed             = False
        self._counter               = 0
        self._buzzer                = Pin(buzzer_pin, Pin.OUT)
        self._dic_process_counter   = {"closed-door": 5, "opened-dorr": 10, "semi-closed-door": 1, "solution-intrusion": 5, "first-time-config": 3, "minimun-presence": 5}
        self._dic_process_beep      = {"intrusion": 15}

    def start_counter(self, name_process):
        self.release_thread()
        self.set_on_process(name_process)
        self._counter  =  self._dic_process_counter[name_process]
        
        _thread.start_new_thread(self.counter, ())
    
    def start_beep(self, name_process):
        self.release_thread()
        self.set_on_process(name_process)
        
        _thread.start_new_thread(self.beep, (self._dic_process_beep[name_process],))
    
    def release_thread(self):
        if(self._control_running):
            self.wait_terminate()
            self.set_off_process()

    def set_on_process(self, name_process):
        self._current_process   = name_process
        self._control_running   = True
        self._running           = True
        self._completed         = False
    
    def set_off_process(self):
        self._control_running   = False
        self._running           = False
        self._counter           = 0
        self._completed         = False
        self._buzzer.off()
    
    def finish_process(self):
        # self._control_running    = False
        self._running            = False
        self._counter            = 0
        self._completed          = True
        self._buzzer.off() 
        
    def counter(self):
        while(self._counter > 0 and self._control_running):
            Util.wait_sec(1)
            self._counter -= 1 

        self.finish_process()
        print("Sai")
    
    def beep(self, beep_per_second):
        aux_calc = int(1000/beep_per_second)
        while(self._control_running):
            Util.wait_ms(aux_calc)
            self._buzzer.toggle()

        self.finish_process()
    
    def wait_terminate(self):
        while self._running == True: 
            Util.wait_ms(10)

    def check_process(self, process):
        return self._current_process == process
    
    def is_running(self):
        return self._running

    def is_completed(self):
        return self._completed
    
    def get_counter(self):
        return self._counter