# robosoft

Human interface for the Botwurst


global_data.py
Definitions and state to be shared by:
    ui_hub.py
    ui_map.py
    ui_display.py


gamepad_interface.py
Read button events from gamepad and print to stdout.


ui_hub.py
Read button events via pipe from gamepad_interface
Send them to ui_map.py
Call ui_display.py


ui_map.py
Get button events from ui_hub
Write and read global_data
Send pin settings to mctransmitter
*** ignores message returned by mctransmitter ***
*** this should somehow be fed back into global_data ***


mctransmitter.py
Recieve pin settings from ui_map and send them over serial to botwurst_a
Returns confirmation message recieved over serial


botwurst_a
Arduino code. Recieve pin settings over serial, set pins, and send confirmation
back over serial


ui_display.py
Print status of global_data to screen.
Simple ascii display.
Might want to replace this with something prettier.

