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
                mctransmitter.tx_analog(0, button_value)
            if (button_index == global_data.AXIS_RIGHT_TRIGGER):
                mctransmitter.tx_analog(1, button_value)



class lock_analog_map(map_interface):

    description = """Lock analog map:

X   -> Hold for Motor 1
Y   -> Hold for Motor 2
A   -> Lock/unlock L1
B   -> Lock/unlock L2
L2  -> Wavelength
R2  -> Frequency"""

    def update(self, button_type, button_index, button_value):
        if (button_type == global_data.TYPE_BUTTON):
            if (button_index == global_data.BUTTON_X):
                mctransmitter.tx_digital(0, button_value)
            elif (button_index == global_data.BUTTON_Y):
                mctransmitter.tx_digital(1, button_value)
            elif ((button_index == global_data.BUTTON_A) and button_value):
                global_data.axis_0_locked = not global_data.axis_0_locked
            elif ((button_index == global_data.BUTTON_B) and button_value):
                global_data.axis_1_locked = not global_data.axis_1_locked
        elif (button_type == global_data.TYPE_AXIS):
            if ((button_index == global_data.AXIS_LEFT_TRIGGER) and not global_data.axis_0_locked):
                mctransmitter.tx_analog(0, button_value)
            if ((button_index == global_data.AXIS_RIGHT_TRIGGER) and not global_data.axis_1_locked):
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
        


 

map_list = [basic_map(), lock_analog_map(), simple_map()]

