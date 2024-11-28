import time
from . import max30100

mx30 = max30100.MAX30100()
mx30.enable_spo2()
mx30.read_sensor()

def getSpo2():
    if mx30.red != mx30.buffer_red:
        spo2 = int((mx30.red / 100))
        spo22 = spo2*0.6787
        return spo22
    else:
        return None

def getPulse():
    if mx30.ir != mx30.buffer_ir :
        hb = int((mx30.ir / 100))
        hbb = hb*0.398
        return hbb
    else:
        return None


# while 1:
#     mx30.read_sensor()

#     mx30.ir, mx30.red

#     hb = int((mx30.ir / 100))
#     spo2 = int((mx30.red / 100))
#     hbb = hb*0.398
#     spo22 = spo2*0.6787
    
#     if mx30.ir != mx30.buffer_ir :
#         print("Pulse:",int(hbb));
#     if mx30.red != mx30.buffer_red:
#         print("SPO2:",int(spo22));

#     time.sleep(2)
