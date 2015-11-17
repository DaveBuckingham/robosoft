
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

    # GET DESCRIPTION OF THE CURRINT CONTROL MAP
    mode_text = ui_map.map_list[global_data.map_index].description.split('\n')

    # 8 = NUMBER OF ROWS WE WILL PRINT
    mode_text += [''] * (8 - len(mode_text))



    # BUILD STRING TO PRINT

    out =  ("\n")
    out += ("                     TRANSMITTED                                MODE")
    out += ("\n")

    FORMAT = "%-12s %-34s %-20s\n"

    out += FORMAT % ("analog_0",
        __bar__(global_data.analog_0_sent),
        mode_text[0])
    out += FORMAT % ("", "", mode_text[1])

    out += FORMAT % ("analog_1",
        __bar__(global_data.analog_1_sent),
        mode_text[2])
    out += FORMAT % ("", "", mode_text[3])

    out += FORMAT % ("digital_0",
        __bar__(global_data.digital_0_sent),
        mode_text[4])
    out += FORMAT % ("", "", mode_text[5])

    out += FORMAT % ("digital_1",
        __bar__(global_data.digital_1_sent),
        mode_text[6])
    out += FORMAT % ("", "", mode_text[7])


    # CLEAR SCREEN
    if (os.name == 'posix'):
        os.system('clear')
    else:
        # NOT SURE ABOUT WINDOWS
        os.system('clear') 

    # PRINT THE STRING
    print out

