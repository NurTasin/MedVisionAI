from pyfirmata import SERVO,Arduino
import time
from logger import *

port='COM6'

board=Arduino(port)

ser_1=8
ser_2=9
ser_3=10
ser_4=11
ser_5=12
ser_covot=7

board.digital[ser_1].mode=SERVO
board.digital[ser_2].mode=SERVO
board.digital[ser_3].mode=SERVO
board.digital[ser_4].mode=SERVO
board.digital[ser_5].mode=SERVO
board.digital[ser_covot].mode=SERVO
def dropMed(names):
    for med in names:
        if "ace" in med.lower():
            LOG(f"Droping {med}")
            board.digital[ser_1].write(90)
            time.sleep(1)
            board.digital[ser_1].write(0)
        elif "amodis" in med.lower():
            LOG(f"Droping {med}")
            board.digital[ser_2].write(90)
            time.sleep(1)
            board.digital[ser_2].write(0)
        elif "maxpro" in med.lower():
            LOG(f"Droping {med}")
            board.digital[ser_3].write(90)
            time.sleep(1)
            board.digital[ser_3].write(0)
        elif "ciprocin" in med.lower():
            LOG(f"Droping {med}")
            board.digital[ser_4].write(90)
            time.sleep(1)
            board.digital[ser_4].write(0)
        elif "alatrol" in med.lower():
            LOG(f"Droping {med}")
            board.digital[ser_5].write(90)
            time.sleep(1)
            board.digital[ser_5].write(0)



def toggleCovotServo(val):
    if val==1:
        board.digital[ser_covot].write(60)
    elif val==0:
        board.digital[ser_covot].write(0)


if __name__=="__main__":
    dropMed(["Ace Extra","Amodis 500","maxpro","ciprocin","AlaTrol XR 500mg"])