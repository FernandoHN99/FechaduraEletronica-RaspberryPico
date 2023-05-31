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
        self._buzzer                = Pin(9, Pin.OUT)
        self._pino_rele             = Pin(8, Pin.OUT)
        self._pino_botao            = Pin(27, Pin.OUT)
        self._thread01              = Thread(self._buzzer)
        self._dic_y_config          = {"minimun": 0, "limit": 33, "increment": 11, "reset":-11}
        self._list_cards            = list_cards
        self._card                  = None
        self._current_y_msg         = None
        self._time_flow_control     = 10

    def run(self):
        # Display
        self._pino_rele.on()
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
    
    def beep_opened_door(self):
        self._buzzer.on()
        Util.wait_ms(80)
        self._buzzer.off()
        Util.wait_ms(40)
        self._buzzer.on()
        Util.wait_ms(80)
        self._buzzer.off()
    
    def calc_y_msg(self):
        if(self._current_y_msg == self._dic_y_config["limit"]):
            self._current_y_msg = self._dic_y_config["minimun"] 
        else:
            self._current_y_msg +=self._dic_y_config["increment"]
    
    def reset_y_msg(self):
        self._display01.clear()
        self._current_y_msg = self._dic_y_config["reset"]
    
    def flow_permission_button(self):     
        if(self._pino_botao.value() == 1): #Estado do botao de dentro for apertado 
            self.flow_allowed_access()

    def closed_door(self):
        self._buzzer.on()
        self._display01.clear() 
        self._display01.write("PORTA", 40, 5)
        self._display01.write("TRANCADA", 30, 20)
        self._display01.show()
        Util.wait_sec(0.75)
        self._buzzer.off()
        self._display01.write_blank()

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

    def msg_allowed_door(self):
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
    
    def msg_sulution_completed(self):
        self._display01.clear()
        self._display01.write("TUDO CERTO", 20, 13)
        self._display01.show()
        Util.wait_sec(1)
        self._display01.write_blank()
    
    def msg_not_authorized(self):
        self._display01.clear()
        self._display01.write("NAO", 55, 5)
        self._display01.write("AUTORIZADO", 30, 18)
        self._display01.show()
        Util.wait_sec(2)
        self._display01.write_blank()
    
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
                            self.closed_door()
                            self._thread01.reset()
                            return
                            
                        else:
                            self._thread01.start_counter("first-time-config")
                    
                    else:
                        self._thread01.start_counter("first-time-config")
                        
                        
                if(self._infrared01.get_state() == 0):
                    self.msg_first_initialization_02()
                    self._thread01.reset()

            self.msg_first_initialization_01()
            self._thread01.reset()

    def flow_intrusion(self):
        self._infrared01.update_state()
        self.reset_y_msg()
        while(self._infrared01.get_state() == 1):
            self.time_flow()
            
            while(self._tag01.read_card() in self._list_cards):
                self.time_flow()

                if(self._thread01.check_process("solution-intrusion")):
                    
                    if(self._thread01.is_running()):
                        self.msg_intrusion_solution()
                        self.reset_y_msg()

                    elif(self._thread01.is_completed()):
                        self._display01.write_blank()
                        self.msg_sulution_completed()
                        self.flow_allowed_access()
                        return

                    else:
                        self._thread01.start_counter("solution-intrusion")
                        self._display01.write_blank()

                else:
                    self._thread01.start_counter("solution-intrusion")
                    self._display01.write_blank()
                    
            if not self._thread01.check_process("intrusion"):
                self._thread01.start_beep("intrusion")
            
            self.msg_intrusion()

    def flow_allowed_access(self):
        self.beep_opened_door()
        self._thread01.reset()   
        self._infrared01.init_helper()
        while(True):
            self._infrared01.update_state()

            # Verifica se é a primeira vez que porta está aberta
            if(self._infrared01.get_state() == 1 and self._infrared01.get_last_state() == 0):
                self._thread01.start_counter("opened-door")
                self._infrared01.set_last_state(1)
                self._pino_rele.on()                           
                
            # Verifica se a se a porta está aberta porem nao eh a primeira vez
            elif(self._infrared01.get_state() == 1 and self._infrared01.get_last_state() == 1): 

                if(self._thread01.check_process("opened-door") and self._thread01.is_running()):
                    self.msg_opened_door()

                elif(self._thread01.check_process("close-door")):
                        self.msg_close_door()

                else:
                    self._thread01.start_beep("close-door")
                    
            # Verifica se é a primeira vez porta está fechada
            elif(self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 1):  
                self._infrared01.set_last_state(0)
    
                if(self._thread01.check_process(None)):
                    self._thread01.start_counter("allowed-door")
                    self._pino_rele.off()
                else:
                    self._thread01.start_counter("semi-closed-door")

            # Verifica se a porta está fechada porem nao eh a primeira vez
            elif(self._infrared01.get_state() == 0 and self._infrared01.get_last_state() == 0):
                
                if(self._thread01.check_process("allowed-door")):

                    if(self._thread01.is_running()):
                        self.msg_allowed_door()

                    else:
                        self._pino_rele.on()
                        self.closed_door()
                        self._display01.write_blank()
                        self._thread01.reset()
                        return

                elif(self._thread01.is_completed()):
                    
                    self.closed_door()
                    self._display01.write_blank()
                    self._thread01.reset()
                    return

                else:
                    self.msg_wait_close_door()


    # Monitoramento Maçaneta
    def start_track(self):
        self.flow_init()
        while(True):
            self.time_flow()
            self._infrared01.update_state()
            self._pir01.update_state()
            
            if(self._pir01.get_state() == 1 and self._pir01.get_last_state() == 0):  # Verifica se ocorreu uma borda de subida
                self._pir01.set_last_state(1)
                i = 0
                
                while(i<= 15 or (self._pir01.get_state() == 1 and self._pir01.get_last_state() == 1)):
                    i +=1
                    self._pir01.update_state()
                    self.msg_person_detected()
                    self.flow_permission_button()
                    self.flow_intrusion()
                    self._card = self._tag01.read_card()
                    self.flow_permission_button()


                    if(self._card in self._list_cards):
                        self.flow_allowed_access()
                        break

                    elif(self._card != None):
                        self.msg_not_authorized()


            if(self._pir01.get_state() == 0 and self._pir01.get_last_state() == 1):  # Verifica se ocorreu uma borda de descida
                self._pir01.set_last_state(0)                                            # Atualiza o estado anterior do senso
                self._display01.write_blank()

            self.flow_intrusion()
            self.flow_permission_button()

if __name__ == '__main__':
     cards=[296151778]
     System(cards).run()