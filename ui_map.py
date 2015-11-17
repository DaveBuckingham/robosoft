
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


class trigger_map(map_interface):

    description = """Triggers control map:

X   -> Hold for Motor 1
A   -> Hold for Motor 2
L2  -> Wavelength
R2  -> Frequency"""

    def update(self, button_type, button_index, button_value):
        if (button_type == global_data.TYPE_BUTTON):
            if (button_index == global_data.BUTTON_X):
                mctransmitter.tx_digital(0, button_value)
            elif (button_index == global_data.BUTTON_A):
                mctransmitter.tx_digital(1, button_value)
        elif (button_type == global_data.TYPE_AXIS):
            if (button_index == global_data.AXIS_LEFT_TRIGGER):
                mctransmitter.tx_analog(0, button_value)
            if (button_index == global_data.AXIS_RIGHT_TRIGGER):
                mctransmitter.tx_analog(1, button_value)
 



class simple_map(map_interface):

    description = """Simple control map:

X    -> Hold for Motor 1
A    -> Hold for Motor 2
Joy1 -> Wavelength
Joy2 -> Frequency"""

    def update(self, button_type, button_index, button_value):
        if (button_type == global_data.TYPE_BUTTON):
            if (button_index == global_data.BUTTON_X):
                mctransmitter.tx_digital(0, button_value)
            elif (button_index == global_data.BUTTON_A):
                mctransmitter.tx_digital(1, button_value)
        elif (button_type == global_data.TYPE_AXIS):
            if (button_index == global_data.AXIS_Y_RIGHT_STICK):
                mctransmitter.tx_analog(0, button_value)
            if (button_index == global_data.AXIS_Y_LEFT_STICK):
                mctransmitter.tx_analog(1, button_value)
        


class toggle_map(map_interface):

    description = """Toggle motor states:

X   -> Toggle Motor 1
A   -> Toggle Motor 2
L2  -> Wavelength
R2  -> Frequency"""

    def update(self, button_type, button_index, button_value):
        if (button_type == global_data.TYPE_BUTTON and button_value == True):
            if (button_index == global_data.BUTTON_X):
                mctransmitter.tx_digital(0, not global_data.digital_0_sent)
            elif (button_index == global_data.BUTTON_A):
                mctransmitter.tx_digital(1, not global_data.digital_1_sent)
        elif (button_type == global_data.TYPE_AXIS):
            if (button_index == global_data.AXIS_Y_RIGHT_STICK):
                mctransmitter.tx_analog(0, button_value)
            if (button_index == global_data.AXIS_Y_LEFT_STICK):
                mctransmitter.tx_analog(1, button_value)
 

 

map_list = [trigger_map(), simple_map(), toggle_map()]

