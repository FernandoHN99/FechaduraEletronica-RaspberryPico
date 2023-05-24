from dir_rfid_RC522.mfrc522 import MFRC522
from dir_util.util import Util


class RFID_RC522:
    def __init__(self, rasp_sck, rasp_miso, rasp_mosi, rfid_cs, rfid_rst, rfid_spi_id):
        self._reader = MFRC522(sck=rasp_sck, miso=rasp_miso, mosi=rasp_mosi, cs=rfid_cs, rst=rfid_rst, spi_id=rfid_spi_id)
    
    def calc_return(self):
        card_result = None
        for card in self._list_control:
            if card is not None:
                return card
        return card_result

    
    def read_card(self):
        self._list_control =[]
        while(len(self._list_control) != 2):
            self._reader.init()
            (stat, tag_type) = self._reader.request(self._reader.REQIDL)
            if stat == self._reader.OK:
                (stat, uid) = self._reader.SelectTagSN()
                if stat == self._reader.OK:
                    self._list_control.append(int.from_bytes(bytes(uid),"little",False))
            else:
                self._list_control.append(None)

        return self.calc_return()
    
