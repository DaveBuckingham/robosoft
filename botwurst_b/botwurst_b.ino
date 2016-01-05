//////////////////////////////////////////////////////////////////
//                                                              //
//                       -- BOTWURST A --                       //
//                                                              //
//                          ALEX COHEN                          //
//                       DAVE BUCKINGHAM                        //
//                                                              //
//       RECIEVES MOTOR COMMANDS OVER USB AND SETS ANALOG       //
//       AND DIGITAL PINS.                                      //
//                                                              //
//////////////////////////////////////////////////////////////////


//////////////////////////////////////
//            CONSTANTS             //
//////////////////////////////////////

#define ANALOG_HI     255

// SERIAL COM
#define SERIAL_DELAY 200  // MILLISECONDS
#define BAUD 9600
#define SERIAL_CONFIG SERIAL_8N1

#define PWM_PIN_0 5
#define PWM_PIN_1 7
#define PWM_PIN_2 9
#define DIRECTION_PIN_0 34
#define DIRECTION_PIN_1 38
#define DIRECTION_PIN_2 42

#define EXPAND 0
#define CONTRACT 1


//////////////////////////////////////
//           VARIABLES              //
//////////////////////////////////////

// STORAGE FOR DATA READ FROM SERIAL COM
char cmd_type;
byte cmd_index;
byte cmd_value;
unsigned long long_cmd_value;

// MILLISECONDS
unsigned long segment_offset;
unsigned long contraction_time;
unsigned long contracted_delay;
unsigned long expansion_time;
unsigned long expanded_delay;

// [0..255]
byte contraction_speed;
byte expansion_speed;

byte paused;

union buffer_u {
    byte byte_array[4];
    unsigned long long_number;
} buffer;

void read_to_buffer() {
    buffer.byte_array[0] = Serial.read();
    buffer.byte_array[1] = Serial.read();
    buffer.byte_array[2] = Serial.read();
    buffer.byte_array[3] = Serial.read();
    return
}


//////////////////////////////////////
//           INTIIALIZE             //
//////////////////////////////////////

void setup() {

    segment_offset = 0;
    contraction_time = 0;
    contracted_delay = 0;
    expansion_time = 0;
    expanded_delay = 0;
    contraction_speed = 0;
    expansion_speed = 0;
    paused = 1;

    // INTIALIZE SERIAL COM
    Serial.begin(BAUD, SERIAL_CONFIG);
    
    // INITIALIZE COMPUTATION AND GPIO
    pinMode(PWM_PIN_0, OUTPUT);
    pinMode(PWM_PIN_1, OUTPUT);
    pinMode(PWM_PIN_2, OUTPUT);
    pinMode(DIRECTION_PIN_0, OUTPUT);
    pinMode(DIRECTION_PIN_1, OUTPUT);
    pinMode(DIRECTION_PIN_2, OUTPUT);

}


//////////////////////////////////////
//            MAIN LOOP             //
//////////////////////////////////////

void loop() {

    //////////////////////////
    // RECEIVE TRANSMISSION //
    //////////////////////////

    // READ TYPE
    if (! Serial.available()) {
        return;
    }
    cmd_type = Serial.read();

    if (cmd_type == 'p') {
        paused = 1;
    }
    else if (cmd_type == 'u') {
        paused = 0;
    }
    else if ((cmd_type == 't') && paused) {
        delay(SERIAL_DELAY);
        read_to_buffer();  segment_offset = buffer.long_number;
        read_to_buffer();  contraction_time = buffer.long_number;
        read_to_buffer();  contracted_delay = buffer.long_number;
        read_to_buffer();  expansion_time = buffer.long_number;
        read_to_buffer();  expanded_delay = buffer.long_number;
        contraction_speed = Serial.read();
        expansion_speed = Serial.read();
    }

}


