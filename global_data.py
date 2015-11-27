ANALOG_MAX = 255

# COMMANDS SENT TO ARDUINO
analog_0_sent  = 0;
analog_1_sent  = 0;
digital_0_sent = False;
digital_1_sent = False;

# RECORD MODE
record = False
record_file_number = None   # None if not recording
record_array = []           # List that stores quads (PIN TYPE, PIN INDEX, value, time step)
record_start_time = None

playback_array = []         # Populated from a recording file, for playback
playback_paused = False
playback_cancel = False


# BUTTON TYPES
TYPE_BUTTON          = 'b'  # VALUE WILL BE 0 OR 1
TYPE_AXIS            = 'a'  # VALUE WILL BE BETWEEN 0 AND 1
TYPE_DPAD            = 'd'  # VALUE WILL BE PAIR OF -1, 0, OR 1

# BUTTON NAMES
BUTTON_A             = 0
BUTTON_B             = 1
BUTTON_X             = 2
BUTTON_Y             = 3
BUTTON_LEFT_BUMPER   = 4
BUTTON_RIGHT_BUMPER  = 5
BUTTON_SELECT        = 6
BUTTON_START         = 7
BUTTON_LEFT_STICK    = 8
BUTTON_RIGHT_STICK   = 9


AXIS_X_LEFT_STICK    = 0
AXIS_Y_LEFT_STICK    = 1
AXIS_LEFT_TRIGGER    = 2
AXIS_X_RIGHT_STICK   = 3
AXIS_Y_RIGHT_STICK   = 4
AXIS_RIGHT_TRIGGER   = 5

D_PAD                = 0


# INDEX TO THE CURRENT CONTROL MAP
# ARRAY DEFINED IN ui_map.py
map_index = 0




# ONLY USED BY ui_map:
axis_0_locked = False
axis_1_locked = False

