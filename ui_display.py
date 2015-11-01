
import os
import global_state   # SHARED WITH ui_display AND ui_map



###############################
#  UPDATE STATUS DISPLAY -db  #
###############################

# DRAW A BAR, FOR EXAMPLE:
# 128  ||||||||||..........
def bar(val):
   # TOTAL LENGTH OF RETURNED STRING IS 25
   length = 20
   if (isinstance(val, bool)):
       if (val):
           return "%3s  " % 'T' + "|"*length
       else:
           return "%3s  " % 'F' + "."*length
   else:
       full = (length * val) / ANALOG_MAX
       return "%3d  " % val + ("|" * full) + ("." * (length - full))

# UPDATE DISPLAY
def display():

    # CLEAR SCREEN
    if (os.name == 'posix'):
        os.system('clear')
    else:
        # NOT SURE ABOUT WINDOWS
        os.system('clear') 

    # FOR TESTING
    mode_description = """DAVE'S AWESOME CONTROL MODE:

L2  -> Wavelength
R2  -> Frequency
X   -> Toggle Motor 1
A   -> Hold for Motor 2
"""
    mode_text = mode_description.split('\n')

    # FOR REAL
    #mode_text = mode.description.split('\n')

    # 7 = NUMBER OF ROWS WE WILL PRINT
    mode_text += [''] * (7 - len(mode_text))

    # HEADDER
    print("\n")
    print("                     TRANSMITTED                    CONFIRMED                         MODE")
    print("\n")

    __FORMAT__ = "%-12s %-30s %-34s %-20s"

    print __FORMAT__ % ("analog_0",  bar(analog_0),  bar(analog_0_confirmed),  mode_text[0])
    print __FORMAT__ % ("",          "",             "",                       mode_text[1])
    print __FORMAT__ % ("analog_1",  bar(analog_1),  bar(analog_1_confirmed),  mode_text[2])
    print __FORMAT__ % ("",          "",             "",                       mode_text[3])
    print __FORMAT__ % ("digital_0", bar(digital_0), bar(digital_0_confirmed), mode_text[4])
    print __FORMAT__ % ("",          "",             "",                       mode_text[5])
    print __FORMAT__ % ("digital_1", bar(digital_1), bar(digital_1_confirmed), mode_text[6])

    print "\n"
    print "here is some more status info e.g. number gamepads connected"
    print "Use 'select' button to cycle control modes."


display()
