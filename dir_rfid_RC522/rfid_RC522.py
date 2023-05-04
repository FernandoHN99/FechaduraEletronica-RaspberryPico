from mfrc522 import MFRC522
from dir_util.util import Util

class RFID_RC522:
    def __init__(self, rasp_sck, rasp_miso, rasp_mosi, rfid_cs, rfid_rst, rfid_spi_id):
        self._reader = MFRC522(sck=rasp_sck, miso=rasp_miso, mosi=rasp_mosi, cs=rfid_cs, rst=rfid_rst, spi_id=rfid_spi_id)
        self._paused = None

    def start(self):
        self._reader.init()

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False
    
    def read_card(self):
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                return int.from_bytes(bytes(uid),"little",False)
        #     else:
        #         print("RFID Error 02")
        # else:
        #     print("RFID Error 01")

 