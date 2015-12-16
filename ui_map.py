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

    #Question: put this in global data?

    dict_return_values = dict.fromkeys(global_data.dict_return_value_keys)
    
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
        return_values = None

        if (button_type == global_data.TYPE_BUTTON):
            if (button_index == global_data.BUTTON_X):
                return_values = ('d',0, button_value)
            elif (button_index == global_data.BUTTON_Y):
                return_values = ('d',1, button_value)
            elif ((button_index == global_data.BUTTON_A) and button_value):
                return_values = ('d',0, not global_data.digital_0_sent)
            elif ((button_index == global_data.BUTTON_B) and button_value):
                return_values = ('d',1, not global_data.digital_1_sent)
        elif (button_type == global_data.TYPE_AXIS):
            if (button_index == global_data.AXIS_LEFT_TRIGGER):
                tx_value = 127 - (button_value / 2)
                return_values = ('a',0, tx_value)
            if (button_index == global_data.AXIS_RIGHT_TRIGGER):
                tx_value = 127
                if (button_value > 0.0):
                    tx_value = 128 + (button_value / 2)
                return_values = ('a',0, tx_value)

        # TODO: FIGURE OUT WHY THIS IS HAPPENING
        if return_values is None:
            print "FOUND SOMETHING WEIRD"
            return None

        basic_map.dict_return_values.update(dict(zip(global_data.dict_return_value_keys, return_values)))

        return basic_map.dict_return_values

map_list = [basic_map()]

