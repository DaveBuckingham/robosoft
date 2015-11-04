
import global_data

class map_interface:

    description = "Default map description"

    def update(self, button, val):
        raise NotImplementedError()


# simple_map AND toggle_map ARE TOY EXAMPLES

class simple_map(map_interface):

    description = """Dave's simple map:

X   -> Hold for Motor 1
A   -> Hold for Motor 2
L2  -> Wavelength
R2  -> Frequency"""

    def update(self, button, val):
        if (button == global_data.BUTTON_X):
            global_data.digital_0 = val
            mctransmitter.tx_digital(0, val)
        elif (button == global_data.BUTTON_A):
            global_data.digital_1 = val
            mctransmitter.tx_digital(1, val)
        elif (button == global_data.AXIS_0):
            global_data.analog_0 = val
            mctransmitter.tx_analog(0, val)
        elif (button == global_data.AXIS_1):
            global_data.analog_1 = val
            mctransmitter.tx_analog(1, val)
        

class toggle_map(map_interface):

    description = """Toggle motor states:

X   -> Toggle Motor 1
A   -> Toggle Motor 2
L2  -> Wavelength
R2  -> Frequency"""

    def update(self, button, val):
        if ((button == global_data.BUTTON_X) and val):
            global_data.digital_0 = not global_data_digital_0
            mctransmitter.tx_digital(0, global_data.digital_0)
        elif (button == global_data.BUTTON_A and val):
            global_data.digital_1 = not global_data_digital_1
            mctransmitter.tx_digital(1, global_data.digital_1)
        elif (button == global_data.AXIS_0):
            global_data.analog_0 = val
            mctransmitter.tx_analog(0, val)
        elif (button == global_data.AXIS_1):
            global_data.analog_1 = val
            mctransmitter.tx_analog(1, val)
 






