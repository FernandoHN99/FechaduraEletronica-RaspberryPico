from dir_rfid_RC522.mfrc522 import MFRC522
from dir_util.util import Util
import utime

reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=17,rst=22)
 
print("Bring TAG closer...")
print("")
 
cont = 0
while True:
    cont+=1
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            print("CARD ID: "+str(card))
    else: 
        print("Nulo")
    
            

    


