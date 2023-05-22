from dir_display_oled.display_oled import Display_Oled
from dir_motion_detector.motion_detector import Motion_Detector
from dir_rfid_RC522.rfid_RC522 import RFID_RC522
from dir_infrared_detector.infrared_detector import Infrared_Detector
from dir_util.util import Util
from dir_util.thread_counter import Thread_Counter
from machine import Pin, SPI

display01             = Display_Oled(rasp_sck=6, rasp_mosi=3, rasp_miso=4, display_dc=4, display_rst=1, display_cs=5)
pir01                 = Motion_Detector(raspberry_pin=14)
infrared01            = Infrared_Detector(raspberry_pin=15, debounce_time=10, interruption_mode=False)
tag01                 = RFID_RC522(rasp_sck=18, rasp_miso=16, rasp_mosi=19, rfid_cs=17, rfid_rst=22, rfid_spi_id=0)

# Display
display01.start()

# PIR HC-SR501 - Sensor movimento
pir01.start_detection()

# Tag RFID  --> Inicializado na Instância

# Sensor Infravermelho
infrared01.start_detection()
display01.write_full("!!! SUCESSO !!!", 1, 1)