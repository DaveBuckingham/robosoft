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

// SERIAL COMMUNICATION
#define LOOP_DELAY 10     // MILLISECONDS
#define SERIAL_DELAY 100  // MILLISECONDS
#define BAUD 9600
#define SERIAL_CONFIG SERIAL_8N1

#define ANALOG_HI     255

//The analog input pins on the Mega are A0-A5
#define ANALOG_INPUT_0  A0
#define ANALOG_INPUT_1  A1

//The digital pins on the Mega can also act as analog output
#define ANALOG_PIN_0 10
#define ANALOG_PIN_1 9

#define DIGITAL_PIN_0 6
#define DIGITAL_PIN_1 5 

#define NUM_DIGITAL_PINS 2
#define NUM_ANALOG_PINS 2


//////////////////////////////////////
//           VARIABLES              //
//////////////////////////////////////

char pin_type;
char buffer[16];
byte pin_index;
byte pin_value;


//////////////////////////////////////
//           INTIIALIZE             //
//////////////////////////////////////

void setup() {
    Serial.begin(BAUD);

    pinMode(ANALOG_PIN_0, OUTPUT);
    pinMode(ANALOG_PIN_1, OUTPUT);
    pinMode(DIGITAL_PIN_0, OUTPUT);
    pinMode(DIGITAL_PIN_1, OUTPUT);

    Serial.println("botwurst_a ready...");
}


//////////////////////////////////////
//           MAIN LOOP              //
//////////////////////////////////////

void loop() {

    //////////////////////////
    //     GET PIN TYPE     //
    //////////////////////////
    if (! Serial.available()) {
        return;
    }
    pin_type = Serial.read();
    if (pin_type != 'a' && pin_type != 'd') {
        Serial.print("Invalid pin type.\n");
        return;
    }
    delay(SERIAL_DELAY);  // WAIT FOR PIN INDEX AND VALUE

    if (! Serial.available()) {
        return;
    }

    pin_index = Serial.read();

    if (! Serial.available()) {
        return;
    }

    //////////////////////////
    //    ANALOG PIN        //
    //////////////////////////
    if (pin_type == 'a') {

        // CHECK INDEX BOUNDS
        if (pin_index < 0 || pin_index >= NUM_ANALOG_PINS) {
            Serial.print("Index out of range.\n");
            return;
        }

        // READ PIN VALUE
        pin_value = Serial.read();
        if (pin_value < 0 || pin_value > ANALOG_HI) {
            Serial.print("Pin value out of range.\n");
            return;
        }

        // WRITE TO PIN  (COULD USE ARRAY)
        if (pin_index == 0) {
            analogWrite(ANALOG_PIN_0, pin_value);
        }
        else if (pin_index == 1) {
            analogWrite(ANALOG_PIN_1, pin_value);
        }
    }

    //////////////////////////
    //    DIGITIAL PIN      //
    //////////////////////////
    else {  // pin_type == 'd'

        // CHECK INDEX BOUNDS
        if (pin_index < 0 || pin_index >= NUM_DIGITAL_PINS) {
            Serial.print("Index out of range.\n");
            return;
        }

        // READ PIN VALUE
        pin_value = Serial.read();
        if (pin_value < 0 || pin_value > 1) {
            Serial.print("Pin value out of range.\n");
            return;
        }

        // WRITE TO PIN
        if (pin_index == 0) {
            digitalWrite(DIGITAL_PIN_0, pin_value);
        }
        else if (pin_index == 1) {
            digitalWrite(DIGITAL_PIN_1, pin_value);
        }
    }

    //////////////////////////
    //   SEND CONFIRMATION  //
    //////////////////////////
    sprintf(buffer, "%u %u\n", pin_index, pin_value);
    Serial.print(buffer);

    // delay(LOOP_DELAY);  // IS THIS NEEDED?
}


