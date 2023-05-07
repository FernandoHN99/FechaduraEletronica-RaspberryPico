from dir_rfid_RC522.mfrc522 import MFRC522
from dir_util.util import Util

class RFID_RC522:
    def __init__(self, rasp_sck, rasp_miso, rasp_mosi, rfid_cs, rfid_rst, rfid_spi_id):
        self._reader = MFRC522(sck=rasp_sck, miso=rasp_miso, mosi=rasp_mosi, cs=rfid_cs, rst=rfid_rst, spi_id=rfid_spi_id)

    def start(self):
        self._reader.init()
    
    def read_card(self):
        self._reader.init()
        (stat, tag_type) = self._reader.request(self._reader.REQIDL)
        if stat == self._reader.OK:
            (stat, uid) = self._reader.SelectTagSN()
            if stat == self._reader.OK:
                return int.from_bytes(bytes(uid),"little",False)
            else:
                return None
        else:
            return None

tag01  = RFID_RC522(rasp_sck=6, rasp_miso=4, rasp_mosi=7, rfid_cs=17, rfid_rst=22, rfid_spi_id=0)
# tag01.start()
while(True):
    card = tag01.read_card()
    Util.wait_sec(1)
    print(card)



