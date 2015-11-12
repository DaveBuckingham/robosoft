ANALOG_MAX = 255

# COMMANDS SENT TO ARDUINO
analog_0_sent  = 0;
analog_1_sent  = 0;
digital_0_sent = False;
digital_1_sent = False;

# (CURRENLTY, NOTHING WRITES TO THIS -db)
# RESPONSE RECIEVED FROM ARDUINO
analog_0_confirmed  = 0;
analog_1_confirmed  = 0;
digital_0_confirmed = False;
digital_1_confirmed = False;

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
AXIS_TRIGGERS        = 2
AXIS_X_RIGHT_STICK   = 3
AXIS_Y_RIGHT_STICK   = 4

D_PAD                = 0


# INDEX TO THE CURRENT CONTROL MAP
# ARRAY DEFINED IN ui_map.py
map_index = 0

