from dir_motion_detector.motion_detector import Motion_Detector
from dir_display_oled.display_oled import Display_Oled
from dir_util.util import Util

class System:
    def __init__(self):
        self._display01 = Display_Oled(rasp_sck=2, rasp_mosi=3, rasp_miso=4, display_dc=0, display_rst=1, display_cs=5)
        self._pir01     = Motion_Detector(raspberry_pin=14)

    def run(self):
        self._display01.start()
        self._display01.write_full("Inicializando Display", 40, 3, timer=1)
        self._pir01.start()
        self._display01.write_full("Inicializando Sensor de Movimento", 40, 3, timer=1)
        self.start_track()


    # Monitoramento Maçaneta
    def start_track(self):
        while True:
            # if(not self._pir01.get_interruption_mode()):         # Verifica se a interrupção está desabilitada
            #     self._pir01.set_state(self._pir01.get_state())   
     
            if(self._pir01.get_state() == 1 and self._pir01.get_last_state() == 0):  # Verifica se ocorreu uma borda de subida
                self._pir01.set_state(1)                                             # Atualiza o estado anterior do senso
                self._display01.write_full("Movimento detectado!", 40, 3)
                self._pir01.pause_detection()

                # Códido da tag

                    # Códido do infravermelho

            if(self._pir01.get_state() == 0 and self._pir01.get_last_state() == 1):  # Verifica se ocorreu uma borda de descida
                self._pir01.set_state(0)                                            # Atualiza o estado anterior do senso
                self._display01.write_full("Sem Movimento!", 40, 3)



if __name__ == '__main__':
    sistema = System().run()