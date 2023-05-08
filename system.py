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
        self._list_cards            = list_cards=[296151778]
        self._t1_control            = Thread_Counter()
        self._dic_times_t1          = {"closed": 5, "opened": 10, "semi-closed": 2, "intrusion": 5, "first-time": 3}
        self._dic_y_config          = {"minimun": 0, "limit": 33, "increment": 11, "reset":-11}
        self._time_flow_control     = 10
        self._card                  = None
        self._current_y_msg         = None

    def run(self):
        # Display
        self._display01.start()
        
        # PIR HC-SR501 - Sensor movimento
        self._pir01.start_detection()

        # Tag RFID  --> Inicializado na Instância

        # Sensor Infravermelho
        self._infrared01.start_detection()

        # Inicio do Monitoramento
        self.start_track()
    
    def time_flow(self):
        Util.wait_ms(self._time_flow_control)
    
    def reset_thread(self):
        if self._t1_control.check_thread():
            self._t1_control.stop()
            self._t1_control = Thread_Counter()
    
    def calc_y_msg(self):
        if(self._current_y_msg == self._dic_y_config["limit"]):
            self._current_y_msg = self._dic_y_config["minimun"] 
        else:
            self._current_y_msg +=self._dic_y_config["increment"]
    
    def reset_y_msg(self):
        self._current_y_msg = self._dic_y_config["reset"] 

    def close_door(self):
        self.reset_thread()
        self._display01.clear() 
        # comando para disparar o motor para trancar a porta
        self._display01.write("PORTA", 40, 5)
        self._display01.write("TRANCADA", 30, 20)
        self._display01.show()
        Util.wait_sec(2)
        self._display01.write_blank()
        self._pir01.start_detection()

    def check_indiviual_time(self, key):
        return self._t1_control.get_counter_limit() == self._dic_times_t1[key]
    
    def set_person_detected(self):
        Util.wait_ms(self._time_flow_control)
        self.pir01_detected()
        self._infrared01.update_state()
    
    def msg_opened_door(self):
        self._display01.clear()
        self._display01.write("Porta Aberta", 20, 3)
        self._display01.write(f"{self._t1_control.get_counter()}", 63, 17)
        self._display01.show()

    def msg_closed_door(self):
        self._display01.clear()
        self._display01.write("Acesso Liberado", 6, 3)
        self._display01.write(f"{self._t1_control.get_counter()}", 63, 17)
        self._display01.show()
    
    def msg_close_door(self):
        self._display01.write_blank(timer=0.25)
        self._display01.write("FECHAR A", 30, 5)
        self._display01.write("PORTA", 40, 20)
        self._display01.show()
        Util.wait_sec(0.75)
    
    def msg_wait_close_door(self):
        self._display01.clear()
        self._display01.write("Aguarde", 40, 3)
        self._display01.write(f"{self._t1_control.get_counter()}", 63, 17)
        self._display01.show()
        Util.wait_sec(0.75)

    def msg_person_detected(self):
        self._display01.clear()
        self._display01.write("Aproxime", 30, 5)
        self._display01.write("o cartao!", 28, 18)
        self._display01.show()
    
    def msg_person_undetected(self):
        self._display01.clear()
        self._display01.write_full("Ate mais! ;)", 17, 9, timer=2)
        self._display01.write_blank()
    
    def msg_intrusion_solution(self):
        self._display01.clear()
        self._display01.write("Mantenha o ", 17, 1)
        self._display01.write("cartao por", 17, 12)
        self._display01.write(f"{self._t1_control.get_counter()} segundos", 17, 23)
        self._display01.show()
        self._display01.clear()

    def msg_intrusion(self):
        self.calc_y_msg()
        if(self._current_y_msg != self._dic_y_config["limit"]):
            self._display01.write("!!! INVASAO !!!", 8, self._current_y_msg)
        else:
            self._display01.clear()        
        self._display01.show()
    
    def msg_first_initialization_01(self):
        self._display01.clear()
        self._display01.write("INICIALIZACAO",6, 0)
        self._display01.write("______________",3, 3)
        self._display01.write("Feche a porta!", 6, 21)
        self._display01.show()

    def msg_first_initialization_02(self):
        self._display01.clear() 
        self._display01.write("INICIALIZACAO",6, 0)
        self._display01.write("______________",3, 3)
        self._display01.write("Aproxime o", 18, 15)
        self._display01.write("Cartao", 28, 25)
        self._display01.show()
    
    def flow_init(self):
        while(True):
            self.time_flow()
            self._infrared01.update_state()
            
            while(self._infrared01.get_state() == 0):
                self.time_flow()
                self._infrared01.update_state()

                while(self._infrared01.get_state() == 0 and self._tag01.read_card() in self._list_cards):
                    self._infrared01.update_state()
                    self.time_flow()
                
                    if(self._t1_control.check_thread()):
                    
                        if(self._t1_control.is_running()):
                            self.msg_intrusion_solution()

                        else:
                            self.close_door()
                            return
                    else:
                        self._t1_control.start(self._dic_times_t1["first-time"])

                if(self._infrared01.get_state() == 0):
                    self.msg_first_initialization_02()
                    self.reset_thread()

            self.msg_first_initialization_01()
            self.reset_thread()


    def flow_intrusion(self):
        self.reset_y_msg()
        while(self._infrared01.get_state() == 1):
            self.time_flow()
            
            while(self._tag01.read_card() in self._list_cards):

                self.time_flow()
                if(self._t1_control.check_thread()):
                    
                    if(self._t1_control.is_running()):
                        self.msg_intrusion_solution()
                        self.reset_y_msg()

                    else:
                        self.flow_allowed_access()
                        self.reset_thread()
                        return
                else:
                    self._t1_control.start(self._dic_times_t1["intrusion"])
            
            self.msg_intrusion()
            self.reset_thread()

    
    def flow_allowed_access(self):
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
                    self.msg_close_door()

            # Verifica se é a primeira vez porta está fechada
            elif(self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 1):  
                self._infrared01.set_last_state(0)       
            
            # Verifica se a porta está fechada porem nao eh a primeira vez
            elif(self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 0):
                
                if(self._t1_control.check_thread()):
                
                    if(self.check_indiviual_time("semi-closed")):

                        if(self._t1_control.is_running()):
                            self.msg_wait_close_door()
                        else:
                            self.close_door()
                            break

                    elif(self.check_indiviual_time("opened")):
                        self._t1_control.start(self._dic_times_t1["semi-closed"]) # Thread iniciada
                    elif(self._t1_control.is_running()):
                        self.msg_closed_door()
                    else:
                        self.close_door()     
                        break
            
                else:
                    self._t1_control.start(self._dic_times_t1["closed"]) # Thread iniciada


    # Monitoramento Maçaneta
    def start_track(self):
        self.flow_init()
        while(True):
            self.time_flow()
            self._infrared01.update_state()
            
            if(self._pir01.get_state() == 1 and self._pir01.get_last_state() == 0):  # Verifica se ocorreu uma borda de subida
                self._pir01.set_last_state(1)
                
                while(self._pir01.get_state() == 1 and self._pir01.get_last_state() == 1):
                    self.time_flow()
                    self._infrared01.update_state()
                    self.msg_person_detected()
                    self._card = self._tag01.read_card()

                    if(self._card in self._list_cards):
                        self.flow_allowed_access()

                    elif(self._card != None):
                        self.flow_allowed_access()
                        # self._display01.write_full("Nao autorizado!", 1, 3, timer=2)  

                    self.flow_intrusion()

            elif(self._pir01.get_state() == 0 and self._pir01.get_last_state() == 1):  # Verifica se ocorreu uma borda de descida
                self._pir01.set_last_state(0)                                            # Atualiza o estado anterior do senso
                self.msg_person_undetected()
            
            elif(False): #Estado do botao de dentro for apertado
                #self.flow_allowed_access()
                pass

            self.flow_intrusion()
                

if __name__ == '__main__':
     System().run()

