# Importa a classe Pin da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin

class Motion_Detector:
    def __init__(self, raspberry_pin, interruption_mode=True):
        self._raspberry_pin     = raspberry_pin               # Define o pino do Raspberry Pi Pico conectado ao módulo PIR HC-SR501
        self._interruption_mode = interruption_mode           # Habilita o uso de interrupção para o sensor
        self._detector          = Pin(self._raspberry_pin, Pin.IN)  # Configura o pino da saída digital do sensor
        self._state             = 0                        # Variável global para armazenar o estado atual do sensor
        self._last_state        = 0                        # Variável global para armazenar o estado anterior do sensor

    # Atualiza a variável global pir_state com o valor do pino
    def detector_callback(self, pin):
        self._state = pin.value()
    
    # Inicializa e DESpausa a detecção de movimento
    def start_detection(self):
        if(self._interruption_mode):
            self._detector.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.detector_callback) # Sensor fica aguardando qualquer mudança de estado
        else:
            self.pause_detection()
        self._last_state  = self._detector.value()
        self._state       = self._detector.value()

    # Pausa a detecção de movimento
    def pause_detection(self):
        self._detector.irq(trigger=0)
    
    # Faz com que os valores sejam atualizados constantemente
    def update_state(self):             
        self._state = self._detector.value()

    # Getters && Setters
    def get_state(self):
        return self._state

    def get_detector(self):
        return self._detector

    def get_last_state(self):
        return self._last_state
    
    def get_interruption_mode(self):
        return self._interruption_mode

    def set_state(self, state):
        self._state = state

    def set_last_state(self, last_state):
        self._last_state = last_state





