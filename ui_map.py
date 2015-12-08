#
# TO MAKE A NEW CONTROL MAP JUST:
# 
# 1. SOMEWHERE BELOW CREATE A CLASS THAT EXTENDS map_interface.
#    PERHAPS COPY AND MODIFY toggle_map.
# 
# 2. ADD AN INSTANCE OF YOUR NEW CLASS TO map_list AT THE BOTTOM
#    OF THIS FILE
#



import global_data
import mctransmitter

class map_interface:

    description = "Default map description"

    def update(self, button, val):
        raise NotImplementedError()


class basic_map(map_interface):

    description = """Basic control map:

X   -> Hold for Motor 1
Y   -> Hold for Motor 2
A   -> Toggle Motor 1
B   -> Toggle Motor 2
L2  -> Wavelength
R2  -> Frequency"""

    def update(self, button_type, button_index, button_value):
        if (button_type == global_data.TYPE_BUTTON):
            if (button_index == global_data.BUTTON_X):
                mctransmitter.tx_digital(0, button_value)
            elif (button_index == global_data.BUTTON_Y):
                mctransmitter.tx_digital(1, button_value)
            elif ((button_index == global_data.BUTTON_A) and button_value):
                mctransmitter.tx_digital(0, not global_data.digital_0_sent)
            elif ((button_index == global_data.BUTTON_B) and button_value):
                mctransmitter.tx_digital(1, not global_data.digital_1_sent)
        elif (button_type == global_data.TYPE_AXIS):
            if (button_index == global_data.AXIS_LEFT_TRIGGER):
                tx_value = 127 - (button_value / 2)
                mctransmitter.tx_analog(0, tx_value)
            if (button_index == global_data.AXIS_RIGHT_TRIGGER):
                tx_value = 127
                if (button_value > 0.0):
                    tx_value = 128 + (button_value / 2)
                mctransmitter.tx_analog(0, tx_value)


map_list = [basic_map()]

