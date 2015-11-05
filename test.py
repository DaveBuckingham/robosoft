# THIS TESTS THE PIPELINE AFTER ui_hub INCLUDING:
#   - ui_map.py
#   - ui_display.py
#   - mctransmitter.py
#   - botwurst.ino
#   - led circuit

import mctransmitter
import ui_display
import global_data
import ui_map
import time

delay = 0.1

map = ui_map.simple_map()
mctransmitter.initialize()

i = 0
j = 0
while (True):

    if (i % 2):
        map.update(global_data.BUTTON_X, True)
    else:
        map.update(global_data.BUTTON_X, False)

    val = abs((j % 510) - 255)
    map.update(global_data.AXIS_Y_RIGHT_STICK, val)
    map.update(global_data.AXIS_Y_LEFT_STICK, 255 - val)

    ui_display.update()
    time.sleep(delay)

    i = i + 1
    j = j + 20

