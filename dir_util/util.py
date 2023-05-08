import os
import utime

class Util():

    @staticmethod
    def wait_sec(sec):
        utime.sleep(sec)

    @staticmethod
    def wait_ms(ms):
        utime.sleep_ms(ms)
