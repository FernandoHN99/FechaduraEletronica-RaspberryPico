from dir_util.util import Util
from machine import Pin, SPI
# Importa a classe SSD1306_SPI da biblioteca ssd1306.py
from dir_display_oled.ssd1306 import SSD1306_SPI


class Display_Oled:
    def __init__(self, rasp_sck, rasp_mosi, rasp_miso, display_dc, display_rst, display_cs):
        self._rasp_sck      = rasp_sck       # pino raspberry spi0 sck/clock
        self._rasp_mosi     = rasp_mosi      # pino raspberry spi0 mosi/tx
        self._rasp_miso     = rasp_miso      # pino raspberry spi0 miso/rx
        self._display_dc    = display_dc     # pino display data_comand
        self._display_rst   = display_rst    # pino display reset
        self._display_cs    = display_cs     # pino display chip select
        self._display 		= None

    def start(self):
        spi0 = SPI(0, baudrate=1000000, polarity=1, phase=0, sck=Pin(self._rasp_sck), mosi=Pin(self._rasp_mosi), miso=Pin(self._rasp_miso))
        self._display = SSD1306_SPI(128, 32, spi0, Pin(self._display_dc), Pin(self._display_rst), Pin(self._display_cs))

    def write(self, msg, x, y, color=1):
        self._display.text(msg, x, y, color)

    def write_full(self, msg, x, y, color=1, timer=0):
        self._display.fill(0)
        self.write(msg, x, y, color)
        self._display.show()
        if(timer != 0):
            Util.wait_sec(timer)
            self.write_blank()

    def write_blank(self, timer=0):
        self._display.fill(0)
        self._display.show()
        Util.wait_sec(timer)
        
    def write_blinking(self, msg, x, y, timer_msg, timer_blink=0.25, color=1):
        self.write_blank(timer_blink)
        self.write_full(msg, 1, 3, timer=timer_msg)

    def vline(self, x, y, hgt, color=1):
        self._display.vline(x, y, hgt, color)

    def rectangle(self, xa, ya, xb, yb, color=1):
        self._display.fill_rect(xa, ya, xb, yb, color)
    
    def show(self):
        self._display.show()

    def clear(self):
        self._display.fill(0)