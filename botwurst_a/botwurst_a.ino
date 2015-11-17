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
#define SERIAL_DELAY 100  // MILLISECONDS
#define BAUD 9600
#define SERIAL_CONFIG SERIAL_8N1

#define NUM_DIGITAL_VALS 2
#define NUM_ANALOG_VALS 2

// *** PIERS: YOU MAY WANT TO CHANGE THESE *** //
#define ANALOG_PIN_0 10
#define ANALOG_PIN_1 9
#define DIGITAL_PIN_0 6
#define DIGITAL_PIN_1 5 



//////////////////////////////////////
//           VARIABLES              //
//////////////////////////////////////

// STORAGE FOR DATA READ FROM SERIAL COM
char cmd_type;
byte cmd_index;
byte cmd_value;


//////////////////////////////////////
//           INTIIALIZE             //
//////////////////////////////////////

void setup() {
    // INTIALIZE SERIAL COM
    Serial.begin(BAUD, SERIAL_CONFIG);
    
    // *** PIERS: YOU MIGHT PUT INITIALIZATIN CODE HERE *** //
    // INITIALIZE COMPUTATION AND GPIO
    pinMode(ANALOG_PIN_0, OUTPUT);
    pinMode(ANALOG_PIN_1, OUTPUT);
    pinMode(DIGITAL_PIN_0, OUTPUT);
    pinMode(DIGITAL_PIN_1, OUTPUT);

    //Serial.println("botwurst_a ready...");
}


//////////////////////////////////////
//          COMPUTE                 //
//////////////////////////////////////

// *** PIERS: YOU MIGHT WANT TO PUT YOUR COMPUTATION HERE *** //
// *** THIS WILL GET CALLED EVERY TIME TIME A NEW COMMAND IS RECEIVED *** //
void compute() {

    // ANALOG
    if (cmd_type == 'a') {
        if (cmd_index == 0) {
            analogWrite(ANALOG_PIN_0, cmd_value);
        }
        else if (cmd_index == 1) {
            analogWrite(ANALOG_PIN_1, cmd_value);
        }
    }

    // DIGITAL
    else {  // cmd_type == 'd'
        if (cmd_index == 0) {
            digitalWrite(DIGITAL_PIN_0, cmd_value);
        }
        else if (cmd_index == 1) {
            digitalWrite(DIGITAL_PIN_1, cmd_value);
        }
    }
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
    if (cmd_type != 'a' && cmd_type != 'd') {
        return;
    }

    // WAIT FOR REST OF DATA
    delay(SERIAL_DELAY);
    if (! Serial.available()) {
        return;
    }

    // READ INDEX
    cmd_index = Serial.read();
    if (! Serial.available()) {
        return;
    }

    // READ VALUE
    cmd_value = Serial.read();

    //////////////////////////
    // PROCESS TRANSMISSION //
    //////////////////////////

    // ANALOG PIN
    if (cmd_type == 'a') {

        // CHECK INDEX BOUNDS
        if (cmd_index < 0 || cmd_index >= NUM_ANALOG_VALS) {
            return;
        }

        // CHECK COMMAND BOUNDS
        if (cmd_value < 0 || cmd_value > ANALOG_HI) {
            return;
        }

        // COMPUTE
        else {
            compute();
        }
    }

    // DIGITIAL PIN
    else if (cmd_type == 'd') {

        // CHECK INDEX BOUNDS
        if (cmd_index < 0 || cmd_index >= NUM_DIGITAL_VALS) {
            return;
        }

        // CHECK COMMAND BOUNDS
        if (cmd_value < 0 || cmd_value > 1) {
            return;
        }

        // COMPUTE
        else {
            compute();
        }
    }
}


