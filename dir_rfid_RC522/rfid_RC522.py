from dir_rfid_RC522.mfrc522 import MFRC522
from dir_util.util import Util

class RFID_RC522:
    def __init__(self, rasp_sck, rasp_miso, rasp_mosi, rfid_cs, rfid_rst, rfid_spi_id, list_cards):
        self._reader = MFRC522(sck=rasp_sck, miso=rasp_miso, mosi=rasp_mosi, cs=rfid_cs, rst=rfid_rst, spi_id=rfid_spi_id)
        self._list_cards = list_cards 

    def start(self):
        self._reader.init()

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False
    
    def read_card(self):
        (stat, tag_type) = self._reader.request(self._reader.REQIDL)
        if stat == self._reader.OK:
            (stat, uid) = self._reader.SelectTagSN()
            if stat == self._reader.OK:
                return int.from_bytes(bytes(uid),"little",False)
            else:
                return None
        else:
            return None
    
    def get_list_cards(self):
        return self._list_cards

 
