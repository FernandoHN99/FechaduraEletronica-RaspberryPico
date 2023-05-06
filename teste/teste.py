from dir_display_oled.display_oled import Display_Oled
from dir_motion_detector.motion_detector import Motion_Detector
from dir_rfid_RC522.rfid_RC522 import RFID_RC522
from dir_infrared_detector.infrared_detector import Infrared_Detector
from dir_util.util import Util
from dir_util.thread_counter import Thread_Counter
import _thread




display01       = Display_Oled(rasp_sck=2, rasp_mosi=3, rasp_miso=4, display_dc=0, display_rst=1, display_cs=5)
pir01           = Motion_Detector(raspberry_pin=14)
infrared01      = Infrared_Detector(raspberry_pin=15, debounce_time=10)
tag01           = RFID_RC522(rasp_sck=6, rasp_miso=4, rasp_mosi=7, rfid_cs=17, rfid_rst=22, rfid_spi_id=0, list_cards=[296151778, 2042233364])


# display01.start()
# display01.write_full("Init display", 1, 3, timer=0.2)

# # PIR HC-SR501 - Sensor movimento
# pir01.start_detection()
# display01.write_full("Init Sensor Mov", 1, 3, timer=0.2)

# # Tag RFID              --> Inicializado porém pausado
# tag01.start()
# display01.write_full("Init RFID Tag", 1, 3, timer=0.2)

# Sensor Infravermelho
infrared01.start_detection()
# display01.write_full("Init infra-red", 1, 3, timer=0.2)

t2_opened_door = None
t1_closed_door = None

while(True):  # Verifica se ocorreu uma borda de subida
    if t1_closed_door == None:
        _lock = _thread.allocate_lock() # cria o lock
        counter_limit = 10 # define o limite do contador
        t1_closed_door = Thread_Counter(counter_limit, _lock) # instancia a classe Thread_Counter
        
    
    print("t1_closed_door: ", t1_closed_door.get_counter())
        
    Util.wait_ms(100)

    infrared01.trusted_signal()                   # Pausa o sinal para averiguar que nao foi um erro
    print("Sate: ", infrared01.get_state())
    print("Last State: ", infrared01.get_last_state())

    # Verifica se é a primeira vez que porta está aberta
    if(infrared01.get_state() == 1 and infrared01.get_last_state() == 0):
        print("Primeira vez porta aberta")
        # break


        # if(t1_closed_door != None and t1_closed_door._running):
        #     t1_closed_door.set_running(False)

        # if(t2_opened_door != None and t2_opened_door._running):
        #     t2_opened_door.set_running(False)

        #     print("Criei thread porta aberta!")
        #     t2_opened_door = Thread_Counter(10)  # Thread iniciada
                                    
        infrared01.set_last_state(1)                                      
        

    # Verifica se a se a porta está aberta porem nao eh a primeira vez
    elif(infrared01.get_state() == 1 and infrared01.get_last_state() == 1):
        print("Segunda vez porta aberta")
        # break
        # display01.write_full(f"Segunda vez porta fechada", 1, 3)

        # if(t2_opened_door != None and t2_opened_door.is_running()):
        #     display01.write_full(f"Fechar a porta! {t2_opened_door._counter}", 1, 3)

        # else:
        #     display01.write_full("!!!Fechar a porta!!!", 1, 3, timer=0.75)

    # Verifica se é a primeira vez porta está fechada
    elif(infrared01.get_state() == 0 and infrared01.get_last_state() == 1):
        print("Primeira vez porta fechada")
        # break
        # print("Primeira vez porta fechada")
        # display01.write_full(f"Primeira vez porta fechada", 1, 3)
                   
        infrared01.set_last_state(0)    

    
    # Verifica se a porta está fechada porem nao eh a primeira vez
    elif(infrared01.get_state() == 0 and infrared01.get_last_state() == 0):
        print("Segunda vez porta fechada")
        
        # if(t2_opened_door != None): 
        #     # comando para disparar o motor para trancar a porta
        #     display01.write_full("Porta Trancada!", 1, 3, timer=2)
        #     t2_opened_door.set_running(False)
        #     Util.wait_ms(10)
        #     t2_opened_door = None
        #     t1_closed_door = None
        #     pir01.start_detection()
        #     break

        # elif(t1_closed_door != None): 

        #     if(not t1_closed_door.is_running()):
        #         # comando para disparar o motor para trancar a porta
        #         display01.write_full("Porta Trancada!", 1, 3)
        #         t1_closed_door.set_running(False)
        #         Util.wait_ms(10)
        #         t1_closed_door = None
        #         t2_opened_door = None
        #         pir01.start_detection()            # Sensor movimento volta a detectar
        #         break
        #     else:
        #         display01.write_full(f"Autorizado! {t1_closed_door._counter}", 1, 3)

        # else:
        #     print("Criei thread porta fechada!")
        #     t1_closed_door = None
           
            # t1_closed_door.set_running(False)
            # Util.wait_ms(100)

print("fim")





