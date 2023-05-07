from dir_motion_detector.motion_detector import Motion_Detector
from dir_util.util import Util


# Importa a classe Pin da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin

class Infrared_Detector(Motion_Detector):
    def __init__(self, raspberry_pin, debounce_time, interruption_mode=True):
        super().__init__(raspberry_pin, interruption_mode)
        self._debounce_time  = debounce_time               # Define o tempo de debounce para o sensor em ms

    
    def trusted_signal(self):
        if(super().get_state() != super().get_last_state()):     # Verifica se o estado do sensor mudou 
            Util.wait_ms(self._debounce_time)
            super().update_state()

    # Getters && Setters
    def get_debounce_time(self):
        return self._debounce_time

    def set_debounce_time(self, debounce_time):
        self._debounce_time = debounce_time

