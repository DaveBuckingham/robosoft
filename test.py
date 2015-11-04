import time
import mctransmitter.py

i=0
while(True):
    mctransmitter.tx_analog(0, i % 255)
    mctransmitter.tx_analog(1, 255 - (i % 255))
    i = i + 5
    time.sleep(.01)
