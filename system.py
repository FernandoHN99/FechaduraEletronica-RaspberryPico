from dir_display_oled.display_oled import Display_Oled
from dir_motion_detector.motion_detector import Motion_Detector
from dir_rfid_RC522.rfid_RC522 import RFID_RC522
# from dir_infrared_detector.infrared_detector import Infrared_Detector
from dir_util.util import Util, Thread_Counter

class System:
    def __init__(self):
        self._display01             = Display_Oled(rasp_sck=2, rasp_mosi=3, rasp_miso=4, display_dc=0, display_rst=1, display_cs=5)
        self._pir01                 = Motion_Detector(raspberry_pin=14)
        # self._infrared01            = Infrared_Detector(raspberry_pin=15, debounce_time=10)
        self._tag01                 = RFID_RC522(rasp_sck=10, rasp_miso=12, rasp_mosi=11, rfid_cs=13, rfid_rst=22, rfid_spi_id=0)
        self._list_cards            = [123, 1234, 12345] 
        self._list_no_cards         = [123456]
        self._limit_opened_door     = 10        # tempo para a porta exibir msg de que deve ser fechada
        self._limit_closed_door     = 5         # tempo para a porta fechar automaticamente qdo liberada oprem encostada
        self._counter_opened_door   = None         # variavel de controle
        self._counter_closed_door   = None         # variavel de controle

    def run(self):
        # Display
        self._display01.start()
        self._display01.write_full("Init display", 1, 3, timer=2)
        
        # PIR HC-SR501 - Sensor movimento
        self._pir01.start_detection()
        self._display01.write_full("Init Sensor Mov", 1, 3, timer=2)

        # Tag RFID              --> Inicializado porém pausado
        self._tag01.start()
        self._tag01.pause()
        self._display01.write_full("Init RFID Tag", 1, 3, timer=2)

        # Sensor Infravermelho
        # self._infrared01.start_detection()
        # self._display01.write_full("Inicializando Sensor Infravermelho", 1, 3, timer=2)


        # Inicio do Monitoramento
        self.start_track()
    
    def pir01_detected(self):
        self._pir01.set_last_state(1)                                             # Atualiza o estado anterior do senso
        self._display01.write("Aproxime", 5, 1)
        self._display01.write("a TAG!", 5, 3)
        self._display01.show()
        # self._pir01.pause_detection()
    
    def pir01_undetected(self):
        self._pir01.set_last_state(0)                                            # Atualiza o estado anterior do senso
        self._display01.clear()
        self._display01.write_full("Até mais!", 1, 3, timer=3)               # Somente para testes

    
#     def set_tag01_on(self):
#        pass 

#     def set_tag01_off(self):
#         pass

    # Função quando porta aberta for aberta
    def set_infrared01_detected(self):
        self._infrared01.set_last_state(1)                                             
        self._counter_opened_door = 0          # Inicia a contagem
        self._display01.write_full("Obstáculo removido!", 40, 3)

#     # Função quando porta for fechada
#     def set_infrared01_undetected(self):
#         self._infrared01.set_last_state(0)                                             # Atualiza o estado anterior do sensor
#         self._counter_opened_door = None
#         self._display01.write_full("Obstáculo detectado!", 40, 3)
    
#     # Função quando porta aberta estiver aberta
#     def function_open_door(self):
#         Util.wait_sec(1)
#         self._counter_opened_door += 1
#         if(self._counter_opened_door >= self._limit_opened_door):
#             self._display01.write_full("Fechar a porta!", 40, 3)

#     # Função quando porta aberta estiver fechada porem esta habilitada a ser aberta
#     def function_close_door(self):
#         Util.wait_sec(1)
#         self._counter_closed_door += 1
#         return self._counter_closed_door >= self._limit_closed_door


#     # Monitoramento Maçaneta
    def start_track(self):
        while(self._pir01.get_state() == 1 and self._pir01.get_last_state() == 0):  # Verifica se ocorreu uma borda de subida
            self.pir01_detected()

            while(self._pir01.get_state() == 1):
                card = self._tag01.read_card()
                print("CARD ID: "+str(card))

                if(card in self._list_cards):
                    Util.wait_sec(3)                                    # vermos o cartao no print (depois apagar)
                    self._pir01.pause_detection()                       # pausa o sensor de presenca de pessoas
                    self._counter_closed_door = 0                       # Inicia a contagem
                    self._infrared01.trusted_signal()                   # Pausa o sinal para averiguar que nao foi um erro

                    if(self._infrared01.get_state() == 1 and self._infrared01.get_last_state() == 0):    # Verifica se é a primeira vez que porta está aberta (Sem obstáculo)
                        self.set_infrared01_detected()
                    
                    elif(self._infrared01.get_state() == 1 and self._infrared01.get_last_state() == 1):  # Verifica se a se a porta está aberta porem nao eh a primeira vez
                       self.function_open_door()

                #     elif(self._counter_opened_door is not None and self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 1):  # Verifica se é a primeira vez porta está fechada (Com obstáculo)
                #         self.set_infrared01_undetected()
                #         # comando para disparar o motor para trancar a porta
                #         self._display01.write_full("Porta Trancada!", 40, 3, timer=2)
                #         self._pir01.start_detection()
                #         self._display01.clear()
                #         break                               

                #     elif(self._counter_closed_door is not None and self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 0):  # Verifica se a porta está fechada porem nao eh a primeira vez
                #         if self.function_close_door():
                #             self._counter_closed_door = None
                #             # comando para disparar o motor para trancar a porta
                #             self._display01.write_full("Porta Trancada!", 40, 3, timer=2)
                #             self._pir01.start_detection()
                #             self._display01.clear()
                #             break
                elif(card not in self._list_no_cards):
                    self._display01.write_full("Não autorizado!", 1, 3, timer=3)             


        

        if(self._pir01.get_state() == 0 and self._pir01.get_last_state() == 1):  # Verifica se ocorreu uma borda de descida
            self.pir01_undetected()

if __name__ == '__main__':
     System().run()

