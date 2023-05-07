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
        self._tag01                 = RFID_RC522(rasp_sck=6, rasp_miso=4, rasp_mosi=7, rfid_cs=17, rfid_rst=22, rfid_spi_id=0)
        self._list_cards            = list_cards=[296151778, 2042233364]
        self._t1_control            = Thread_Counter()
        self._dic_times_t1          = {"closed": 5, "opened": 10, "semi-closed": 3, "intrusion": 5}
        self._time_flow_control     = 10
        self._card                  = None

    def run(self):
        # Display
        self._display01.start()
        self._display01.write_full("Init display", 1, 3, timer=0.2)
        
        # PIR HC-SR501 - Sensor movimento
        self._pir01.start_detection()
        self._display01.write_full("Init Sensor Mov", 1, 3, timer=0.2)

        # Tag RFID              --> Inicializado na Instância
        self._display01.write_full("Init RFID Tag", 1, 3, timer=0.2)

        # Sensor Infravermelho
        self._infrared01.start_detection()
        self._display01.write_full("Init infra-red", 1, 3, timer=0.2)

        # Inicio do Monitoramento
        self.start_track()
    
    def time_flow(self):
        Util.wait_ms(self._time_flow_control)
    
    def reset_thread(self):
        if self._t1_control.check_thread():
            self._t1_control.stop()
            self._t1_control = Thread_Counter()
    
    def close_door(self):
        self.reset_thread()
        # comando para disparar o motor para trancar a porta
        self._display01.write_full("Porta Trancada!", 1, 3, timer=2)
        self._pir01.start_detection()

    def check_indiviual_time(self, key):
        return self._t1_control.get_counter_limit() == self._dic_times_t1[key]
    
    def set_person_detected(self):
        Util.wait_ms(self._time_flow_control)
        self.pir01_detected()
        self._infrared01.update_state()
    
    def msg_opened_door(self):
        self._display01.clear()
        self._display01.write("Porta", 20, 3)
        self._display01.write(f"Aberta {self._t1_control.get_counter()}", 20, 15)
        self._display01.show()
    
    def msg_person_detected(self):
        self._display01.clear()                                             # Atualiza o estado anterior do senso
        self._display01.write("Aproxime", 5, 1)
        self._display01.write("a TAG!", 5, 15)
        self._display01.show()
    
    def msg_person_undetected(self):
        self._display01.clear()
        self._display01.write_full("Ate mais! ;)", 1, 3, timer=2)
        self._display01.write_blank()
    
    def msg_intrusion_solution(self):
        self._display01.clear()                                             # Atualiza o estado anterior do senso
        self._display01.write("Mantenha o ", 10, 1)
        self._display01.write("por cartao", 10, 10)
        self._display01.write(f"{self._t1_control.get_counter()} segundos", 10, 20)
        self._display01.show()
    
    def check_invasao(self):
        while(self._infrared01.get_state() == 1):
            self.time_flow()
            
            while(self._tag01.read_card() in self._list_cards):

                self.time_flow()
                if(self._t1_control.check_thread()):
                    
                    if(self._t1_control.is_running()):
                        self.msg_intrusion_solution()

                    else:
                        self.flow_door_handle()
                        self.reset_thread()
                        return
                else:
                    self._t1_control.start(self._dic_times_t1["intrusion"])
            
            self._display01.write_blinking("!! INVASAO !!", 1, 3, timer_msg=0.75)
            self.reset_thread()

    
    def flow_door_handle(self):
        self._t1_control = Thread_Counter()                 # Iniciaiza a thread, porem sem o start
        self._pir01.pause_detection()                       # Pausa o sensor de presenca de pessoas

        while(True):
            self.time_flow()
            self._infrared01.update_state()

            # Verifica se é a primeira vez que porta está aberta
            if(self._infrared01.get_state() == 1 and self._infrared01.get_last_state() == 0):
                self._t1_control.start(self._dic_times_t1["opened"])  # Thread iniciada
                self._infrared01.set_last_state(1)                                      
                
            # Verifica se a se a porta está aberta porem nao eh a primeira vez
            elif(self._infrared01.get_state() == 1 and self._infrared01.get_last_state() == 1): 

                if(self._t1_control.is_running()):
                    self.msg_opened_door()
                else:
                    self._display01.write_blinking("Fechar a porta!!!", 1, 3, timer_msg=0.75)

            # Verifica se é a primeira vez porta está fechada
            elif(self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 1):  
                self._infrared01.set_last_state(0)       
            
            # Verifica se a porta está fechada porem nao eh a primeira vez
            elif(self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 0):
                
                if(self._t1_control.check_thread()):
                
                    if(self.check_indiviual_time("semi-closed")):

                        if(self._t1_control.is_running()):
                            self._display01.write_full(f"Aguarde {self._t1_control.get_counter()}...", 1, 3)
                        else:
                            self.close_door()
                            break

                    elif(self.check_indiviual_time("opened")):
                        self._t1_control.start(self._dic_times_t1["semi-closed"]) # Thread iniciada
                    elif(self._t1_control.is_running()):
                        self._display01.write_full(f"Autorizado! {self._t1_control.get_counter()}", 1, 3)
                    else:
                        self.close_door()     
                        break
            
                else:
                    self._t1_control.start(self._dic_times_t1["closed"]) # Thread iniciada
                                    


    # Monitoramento Maçaneta
    def start_track(self):
        while(True):  # Verifica se ocorreu uma borda de subida
            self.time_flow()
            self._infrared01.update_state()
            
            if(self._pir01.get_state() == 1 and self._pir01.get_last_state() == 0):  # Verifica se ocorreu uma borda de subida
                self._pir01.set_last_state(1)
                
                while(self._pir01.get_state() == 1 and self._pir01.get_last_state() == 1):
                    self.time_flow()
                    self.msg_person_detected()
                    self._card = self._tag01.read_card()

                    if(self._card in self._list_cards):
                        self.flow_door_handle()

                    elif(self._card != None):
                        self._display01.write_full("Nao autorizado!", 1, 3, timer=2)  

                    self.check_invasao()

            elif(self._pir01.get_state() == 0 and self._pir01.get_last_state() == 1):  # Verifica se ocorreu uma borda de descida
                self._pir01.set_last_state(0)                                            # Atualiza o estado anterior do senso
                self.msg_person_undetected()
            
            self.check_invasao()
                

if __name__ == '__main__':
     System().run()
