import mctransmitter
import time

delay = 0.05

mctransmitter.initialize()
while (True):
    mctransmitter.tx_analog(0, 255)
    time.sleep(delay)
    mctransmitter.tx_analog(0, 0)

    mctransmitter.tx_analog(1, 255)
    time.sleep(delay)
    mctransmitter.tx_analog(1, 0)

    mctransmitter.tx_digital(0, 1)
    time.sleep(delay)
    mctransmitter.tx_digital(0, 0)

    #mctransmitter.tx_digital(1, 1)
    #time.sleep(delay)
    #mctransmitter.tx_digital(1, 0)

