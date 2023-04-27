# Importa a classe Pin da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin

class MotionDetector:

    def __init__(self, raspberry_pin, interruption_mode):
        self._raspberry_pin     = raspberry_pin               # Define o pino do Raspberry Pi Pico conectado ao módulo PIR HC-SR501
        self._pir               = Pin(raspberry_pin, Pin.IN)  # Configura o pino da saída digital do sensor
        self._interruption_mode = interruption_mode           # Habilita o uso de interrupção para o sensor
        self._pir_state         = None                        # Variável global para armazenar o estado atual do sensor
        self._pir_last_state    = None                        # Variável global para armazenar o estado anterior do sensor

    # Inicializa o sensor
    def start_pir(self):
        self._pir.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.pir_callback) #Sensor fica aguardando qualquer mudança de estado
        self._pir_state       = self._pir.value()
        self._pir_last_state  = self._pir.value()
        self.show_outputs()
    
    # Atualiza a variável global pir_state com o valor do pino
    def pir_callback(self):
        self._pir_state = pin.value()

    # Exibe continuamente o estado do sensor
    def show_outputs(self):
        while True:
            # if(not self._interruption_mode):         # Verifica se a interrupção está desabilitada
            #     pir_state = pir.value()             

            if(pir_state == 1 and pir_last_state == 0):   # Verifica se ocorreu uma borda de subida
                pir_last_state = 1                        # Atualiza o estado anterior do sensor
                print("Movimento detectado!")

            elif(pir_state == 0 and pir_last_state == 1):   # Verifica se ocorreu uma borda de descida
                pir_last_state = 0                          # Atualiza o estado anterior do sensor
                print("Sem Movimento!")

    def get_pir_state(self):
        return self._pir_state

    def get_pir_last_state(self):
        return self._pir_last_state