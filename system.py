from dir_display_oled.display_oled import Display_Oled
from dir_motion_detector.motion_detector import Motion_Detector
from dir_rfid_RC522.rfid_RC522 import RFID_RC522
from dir_infrared_detector.infrared_detector import Infrared_Detector
from dir_util.util import Util
from dir_thread.thread import Thread
from machine import Pin, SPI

class System:
    def __init__(self, list_cards):
        self._display01             = Display_Oled(rasp_sck=6, rasp_mosi=3, rasp_miso=4, display_dc=4, display_rst=1, display_cs=5)
        self._pir01                 = Motion_Detector(raspberry_pin=14, interruption_mode=False)
        self._infrared01            = Infrared_Detector(raspberry_pin=15, debounce_time=10, interruption_mode=False)
        self._tag01                 = RFID_RC522(rasp_sck=18, rasp_miso=16, rasp_mosi=19, rfid_cs=17, rfid_rst=22, rfid_spi_id=0)
        self._thread01              = Thread(buzzer_pin=9)
        self._pino_rele             = Pin(8, Pin.OUT)
        self._pino_botao            = Pin(27, Pin.OUT)
        self._dic_y_config          = {"minimun": 0, "limit": 33, "increment": 11, "reset":-11}
        self._list_cards            = list_cards
        self._card                  = None
        self._current_y_msg         = None
        self._time_flow_control     = 10


    def run(self):
        # Display
        self._pino_rele.on()
        self._display01.start()
        self._display01.write_full("Display", 10, 10, timer=0.2)
        
        # PIR HC-SR501 - Sensor movimento
        self._pir01.start_detection()
        self._display01.write_full("MOV", 10, 10, timer=0.2)
    
        # Tag RFID  --> Inicializado na Instância

        # Sensor Infravermelho
        self._infrared01.start_detection()
        self._display01.write_full("Infrared", 10, 10, timer=0.2)

        # Inicio do Monitoramento
        self.flow_init()
        # self.start_track()
    
    def time_flow(self):
        Util.wait_ms(self._time_flow_control)
    
    def calc_y_msg(self):
        if(self._current_y_msg == self._dic_y_config["limit"]):
            self._current_y_msg = self._dic_y_config["minimun"] 
        else:
            self._current_y_msg +=self._dic_y_config["increment"]
    
    def reset_y_msg(self):
        self._current_y_msg = self._dic_y_config["reset"]
    
    def flow_permission_button(self):     
        if(self._pino_botao.value() == 1): #Estado do botao de dentro for apertado 
            self.flow_allowed_access()

    def close_door(self):
        self._thread01.release_thread()
        self._display01.clear() 
        self._display01.write("PORTA", 40, 5)
        self._display01.write("TRANCADA", 30, 20)
        self._display01.show()
        Util.wait_sec(2)
        self._display01.write_blank()
        # self._pir01.start_detection()

    def check_indiviual_time(self, key):
        return self._thread01.get_counter_limit() == self._dic_times_t1[key]
    
    def set_person_detected(self):
        Util.wait_ms(self._time_flow_control)
        self.pir01_detected()
        self._infrared01.update_state()
    
    def msg_opened_door(self):
        self._display01.clear()
        self._display01.write("Porta Aberta", 20, 3)
        self._display01.write(f"{self._thread01.get_counter()}", 63, 17)
        self._display01.show()

    def msg_closed_door(self):
        self._display01.clear()
        self._display01.write("Acesso Liberado", 6, 3)
        self._display01.write(f"{self._thread01.get_counter()}", 63, 17)
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
        self._display01.write(f"{self._thread01.get_counter()}", 63, 17)
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
        self._display01.write(f"{self._thread01.get_counter()} segundos", 17, 23)
        self._display01.show()
        self._display01.clear()

    def msg_intrusion(self):
        self.calc_y_msg()
        if(self._current_y_msg != self._dic_y_config["limit"]):
            self._display01.write("!!! INVASAO !!!", 8, self._current_y_msg)
        else:
            self._display01.clear()        
        self._display01.show()
    
    def msg_not_authorized(self):
        self._display01.clear()
        self._display01.write("NAO", 55, 5)
        self._display01.write("AUTORIZADO", 30, 18)
        self._display01.show()
        Util.wait_sec(2)
    
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

                    if(self._thread01.check_process("first-time-config")):

                        if(self._thread01.is_running()):
                            self.msg_intrusion_solution()

                        elif(self._thread01.is_completed()):
                            self.close_door()
                            return
                            
                        else:
                            self._thread01.start_counter("first-time-config")
                    
                    else:
                        self._thread01.start_counter("first-time-config")
                        
                        
                #if(self._infrared01.get_state() == 0):
                self.msg_first_initialization_02()
                self._thread01.release_thread()

            self.msg_first_initialization_01()
            self._thread01.release_thread()


    def flow_intrusion(self):
        self.reset_y_msg()
        self._thread01.release_thread()
        while(self._infrared01.get_state() == 1):
            self.time_flow()
            
            while(self._tag01.read_card() in self._list_cards):

                self.time_flow()
                if(self._thread01.check_thread_counter()):
                    
                    if(self._thread01.is_running()):
                        self.msg_intrusion_solution()
                        self.reset_y_msg()

                    else:
                        self.flow_allowed_access()
                        self._thread01.release_thread()
                        return
                else:
                    self._thread01.start_counter(self._dic_times_t1["intrusion"])
                    
            if not self._thread01.check_thread_beep():
                self._thread01.start_beep(self._dic_beeps_t1["intrusion"])
            
            self.msg_intrusion()

    def flow_allowed_access(self):
        self._thread01.release_thread()                 # Iniciaiza a thread, porem sem o start
        #self._pir01.pause_detection()                       # Pausa o sensor de presenca de pessoas

        while(True):
            self.time_flow()
            self._infrared01.update_state()

            # Verifica se é a primeira vez que porta está aberta
            if(self._infrared01.get_state() == 1 and self._infrared01.get_last_state() == 0):
                self._thread01.start_counter(self._dic_times_t1["opened"])  # Thread iniciada
                self._infrared01.set_last_state(1)
                self._pino_rele.value(1) 
                                   
                
            # Verifica se a se a porta está aberta porem nao eh a primeira vez
            elif(self._infrared01.get_state() == 1 and self._infrared01.get_last_state() == 1): 

                if(self._thread01.check_thread_counter() and self._thread01.is_running()):
                    self.msg_opened_door()
                else:
                    if(not self._thread01.check_thread_beep()):
                        self._thread01.start_beep(2)
                    
                    self.msg_close_door()

            # Verifica se é a primeira vez porta está fechada
            elif(self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 1):  
                self._infrared01.set_last_state(0)

            
            # Verifica se a porta está fechada porem nao eh a primeira vez
            elif(self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 0):
                
                if(self._thread01.check_thread_counter()):
                
                    if(self.check_indiviual_time("semi-closed")):

                        if(self._thread01.is_running()):
                            self.msg_wait_close_door()
                        else:
                            self.close_door()
                            break

                    elif(self.check_indiviual_time("opened")):
                        self._thread01.start_counter(self._dic_times_t1["semi-closed"]) # Thread iniciada
                    elif(self._thread01.is_running()):
                        self.msg_closed_door()
                    else:  
                        self._pino_rele.value(1)
                        self.close_door()
                        break
            
                else:
                    self._thread01.start_counter(self._dic_times_t1["closed"]) # Thread iniciada
                    self._pino_rele.value(0)


    # Monitoramento Maçaneta
    def start_track(self):
        self.flow_init()
        self._thread01.release_thread()
        while(True):
            self.time_flow()
            self._infrared01.update_state()
            self._pir01.update_state()
            
            if(self._pir01.get_state() == 1 and self._pir01.get_last_state() == 0):  # Verifica se ocorreu uma borda de subida
                self._pir01.set_last_state(1)
                self._thread01.start_counter(self._dic_times_t1["minimun-presence"])
                
                while(self._thread01.is_running() or (self._pir01.get_state() == 1 and self._pir01.get_last_state() == 1)):
                    self.time_flow()
                    self._infrared01.update_state()
                    self._pir01.update_state()
                    self.msg_person_detected()
                    self._card = self._tag01.read_card()

                    if(self._card in self._list_cards):
                        self.flow_allowed_access()
                        self._pir01.set_state(0)
                        break

                    elif(self._card != None):
                        self.msg_not_authorized()

                    self.flow_intrusion()
                    self.flow_permission_button()

            elif(self._pir01.get_state() == 0 and self._pir01.get_last_state() == 1):  # Verifica se ocorreu uma borda de descida
                self._pir01.set_last_state(0)                                            # Atualiza o estado anterior do senso
                self.msg_person_undetected()

            self.flow_intrusion()
            self.flow_permission_button()

if __name__ == '__main__':
     cards=[296151778]
     System(cards).run()
