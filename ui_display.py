
import os
import global_data
import ui_map



###############################
#  UPDATE STATUS DISPLAY -db  #
###############################

# DRAW A BAR, FOR EXAMPLE:
# 128  ||||||||||..........
def __bar__(val):
   # TOTAL LENGTH OF RETURNED STRING IS 25
   length = 20
   if (isinstance(val, bool)):
       if (val):
           return "%3s  " % 'T' + "|"*length
       else:
           return "%3s  " % 'F' + "."*length
   else:
       full = (length * val) / global_data.ANALOG_MAX
       return "%3d  " % val + ("|" * full) + ("." * (length - full))

# UPDATE DISPLAY
def update():

    # CLEAR SCREEN
    if (os.name == 'posix'):
        os.system('clear')
    else:
        # NOT SURE ABOUT WINDOWS
        os.system('clear') 

    mode_text = ui_map.map_list[global_data.map_index].description.split('\n')

    # FOR REAL
    #mode_text = mode.description.split('\n')

    # 8 = NUMBER OF ROWS WE WILL PRINT
    mode_text += [''] * (8 - len(mode_text))

    # HEADDER
    print("\n")
    print("                     TRANSMITTED                    CONFIRMED                         MODE")
    print("\n")

    FORMAT = "%-12s %-30s %-34s %-20s"

    print FORMAT % ("analog_0",
        __bar__(global_data.analog_0),
        __bar__(global_data.analog_0_confirmed),
        mode_text[0])
    print FORMAT % ("", "", "", mode_text[1])

    print FORMAT % ("analog_1",
        __bar__(global_data.analog_1),
        __bar__(global_data.analog_1_confirmed),
        mode_text[2])
    print FORMAT % ("", "", "", mode_text[3])

    print FORMAT % ("digital_0",
        __bar__(global_data.digital_0),
        __bar__(global_data.digital_0_confirmed),
        mode_text[4])
    print FORMAT % ("", "", "", mode_text[5])

    print FORMAT % ("digital_1",
        __bar__(global_data.digital_1),
        __bar__(global_data.digital_1_confirmed),
        mode_text[6])
    print FORMAT % ("", "", "", mode_text[7])

    print "\n"
    print "here is some more status info e.g. number gamepads connected"
    print "Use 'select' button to cycle control modes."

