from dir_display_oled.display_oled import Display_Oled
from dir_motion_detector.motion_detector import Motion_Detector
from dir_rfid_RC522.rfid_RC522 import RFID_RC522
from dir_infrared_detector.infrared_detector import Infrared_Detector
from dir_util.util import Util
from dir_util.thread_counter import Thread_Counter

class System:
    def __init__(self):
        self._display01             = Display_Oled(rasp_sck=2, rasp_mosi=3, rasp_miso=4, display_dc=0, display_rst=1, display_cs=5)
        self._pir01                 = Motion_Detector(raspberry_pin=14)
        self._infrared01            = Infrared_Detector(raspberry_pin=15, debounce_time=10, interruption_mode=False)
        self._tag01                 = RFID_RC522(rasp_sck=6, rasp_miso=4, rasp_mosi=7, rfid_cs=17, rfid_rst=22, rfid_spi_id=0, list_cards=[296151778, 2042233364])

        self._t1_closed_door        = None
        self._t2_opened_door        = None

    def run(self):
        # Display
        self._display01.start()
        self._display01.write_full("Init display", 1, 3, timer=0.2)
        
        # PIR HC-SR501 - Sensor movimento
        self._pir01.start_detection()
        self._display01.write_full("Init Sensor Mov", 1, 3, timer=0.2)

        # Tag RFID              --> Inicializado porém pausado
        self._tag01.start()
        self._tag01.pause()
        self._display01.write_full("Init RFID Tag", 1, 3, timer=0.2)

        # Sensor Infravermelho
        self._infrared01.start_detection()
        self._display01.write_full("Init infra-red", 1, 3, timer=0.2)


        # Inicio do Monitoramento
        self.start_track()
    
    def pir01_detected(self):
        self._pir01.set_last_state(1)
        self._display01.clear()                                             # Atualiza o estado anterior do senso
        self._display01.write("Aproxime", 5, 1)
        self._display01.write("a TAG!", 5, 15)
        self._display01.show()
        
        # self._pir01.pause_detection()
    
    def pir01_undetected(self):
        self._pir01.set_last_state(0)                                            # Atualiza o estado anterior do senso
        self._display01.clear()
        self._display01.write_full("Ate mais!", 1, 3, timer=1)               # Somente para testes


#     # Monitoramento Maçaneta
    def start_track(self):
        while(True):  # Verifica se ocorreu uma borda de subida
            Util.wait_ms(100)

            if(self._pir01.get_state() == 1 and self._pir01.get_last_state() == 0):  # Verifica se ocorreu uma borda de subida
                
                while(self._pir01.get_state() == 1 ):
                    Util.wait_ms(100)
                    self.pir01_detected()
                    self._infrared01.update_state()
                    card = self._tag01.read_card()

                    if(card in self._tag01.get_list_cards()):
                        self._pir01.pause_detection()                       # pausa o sensor de presenca de pessoas
                        card = None           

                        while(True):
                            Util.wait_ms(100)
                            self._infrared01.update_state()
                            print("Sate: ", self._infrared01.get_state())
                            print("Last State: ", self._infrared01.get_last_state())

                            # Verifica se é a primeira vez que porta está aberta
                            if(self._infrared01.get_state() == 1 and self._infrared01.get_last_state() == 0):

                                # if(self._t1_closed_door != None and self._t1_closed_door._running):
                                self._t1_closed_door.set_running(False)
                                self._t1_closed_door = None

                                if(self._t2_opened_door != None and self._t2_opened_door._running):
                                    self._t2_opened_door.set_running(False)
                                
                                Util.wait_ms(500)
                                print("Antes")
                                self._t2_opened_door = Thread_Counter(10)  # Thread iniciada
                                print("Depois")
                                self._infrared01.set_last_state(1)                                      
                                

                            # Verifica se a se a porta está aberta porem nao eh a primeira vez
                            elif(self._infrared01.get_state() == 1 and self._infrared01.get_last_state() == 1):

                                print("self._t2_opened_door: ", self._t2_opened_door ) 
                                print("self._t2_opened_door.is_running(): ", self._t2_opened_door.is_running()) 

                                if(self._t2_opened_door != None and self._t2_opened_door.is_running()):
                                    self._display01.write_full(f"Fechar a porta! {self._t2_opened_door._counter}", 1, 3)

                                else:
                                    self._display01.write_full("", 1, 3, timer=0.2)
                                    self._display01.write_full("!!!Fechar a porta!!!", 1, 3, timer=0.75)

                            # Verifica se é a primeira vez porta está fechada
                            elif(self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 1):  
                                self._infrared01.set_last_state(0)                       
                            
                            # Verifica se a porta está fechada porem nao eh a primeira vez
                            elif(self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 0):
                                
                                if(self._t2_opened_door != None):
                                    self._t2_opened_door.set_running(False)
                                    # comando para disparar o motor para trancar a porta
                                    self._display01.write_full("Porta Trancada!", 1, 3, timer=2)
                                    self._pir01.start_detection()
                                    self._t1_closed_door = None
                                    self._t2_opened_door = None
                                    print("BREAK")
                                    break

                                elif(self._t1_closed_door != None):

                                    if(not self._t1_closed_door.is_running()):
                                        self._t1_closed_door.set_running(False)
                                        # comando para disparar o motor para trancar a porta
                                        self._display01.write_full("Porta Trancada!", 1, 3, timer=2)
                                        self._pir01.start_detection()        
                                        self._t1_closed_door = None
                                        self._t2_opened_door = None
                                        print("BREAK")
                                        break

                                    else:
                                        self._display01.write_full(f"Autorizado! {self._t1_closed_door._counter}", 1, 3)
                                
                                else:
                                    self._t1_closed_door = Thread_Counter(5)  # Thread iniciada
                                    
                    elif(card != None):
                        self._display01.write_full("Nao autorizado!", 1, 3, timer=2)  
                                
            elif(self._pir01.get_state() == 0 and self._pir01.get_last_state() == 1):  # Verifica se ocorreu uma borda de descida
                self.pir01_undetected()
            
            else:
                self._display01.write_full("", 1, 3) 


if __name__ == '__main__':
     System().run()





