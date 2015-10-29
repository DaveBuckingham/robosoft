//////////////////////////////////////////////////////////////////
//                                                              //
//                       -- BOTWURST A --                       //
//                                                              //
//                          ALEX COHEN                          //
//                       DAVE BUCKINGHAM                        //
//                                                              //
//       RECIEVES MOTOR COMMANDS OVER USB AND SETS ANALOG       //
//       AND DIGITLA PINS.                                      //
//                                                              //
//////////////////////////////////////////////////////////////////

#define DEBUG

//////////////////////////////////////
//            CONSTANTS             //
//////////////////////////////////////

// SERIAL COMMUNICATION
#define LOOP_DELAY 10  // MILLISECONDS
#define BAUD 9600
#define SERIAL_CONFIG SERIAL_8N1

// PIN IO
#define LOWVOLTAGE 0    //the low boundary for output voltage
#define HIGHVOLTAGE 255 //the high boundary for output voltage
#define OUTPIN0 A0      //The analog pins on the Mega are A0-A5
#define OUTPIN1 A1
#define OUTPIN2 13
#define OUTPIN3 12
#define INPIN 7         // input pin to get feedback from robot


//////////////////////////////////////
//           VARIABLES              //
//////////////////////////////////////

// COMMAND VALUES
byte wave_speed;
byte wavelength;
byte motor_0;
byte motor_1;

// TO HOLD PACKET HEADDER
char flag;

// FOR ITERATING OVER THE FOUR COMMAND VALUES
#define NUM_COMMANDS 4
byte* command_pointers[NUM_COMMANDS];
int i;


//////////////////////////////////////
//        GET MOTOR COMMAND         //
//////////////////////////////////////

// READ 4 BYTES AND STORE IN GLOBAL VARIABLES
// RETURN TRUE IF 4 VALUES READ, ELSE FALSE
boolean get_motor_command () {

    // IF THERE ARE INCOMMING BYTES
    // CHECK FOR START FLAG ':'
    if (! Serial.available()) {
        return false;
    }
    flag = Serial.read();
    delay(100);  // WAIT FOR ALL DATA
    while (flag != ':' && Serial.available()) {
        flag = Serial.read();
    }
    if (flag != ':') {
        return false;
    }

    // ITERATE OVER COMMANDS
    // STORING VALUES READ FROM SERIAL
    for (i= 0; i < NUM_COMMANDS; i++) {
        if (Serial.available()) {
            *command_pointers[i] = Serial.read();
        }
        else {
            return false;
        }
    }

#ifdef DEBUG
    // ECHO THE COMMANDS
    char buffer[20];
    sprintf(buffer, "%u %u %u %u\n", wave_speed, wavelength, motor_0, motor_1);
    Serial.print(buffer);
#endif

    return true;
}


//////////////////////////////////////
//           INTIIALIZE             //
//////////////////////////////////////

void setup() {
    // SET UP INPUT
    Serial.begin(BAUD);
    command_pointers[0] = &wave_speed;
    command_pointers[1] = &wavelength;
    command_pointers[2] = &motor_0;
    command_pointers[3] = &motor_1;
    for (i= 0; i < NUM_COMMANDS; i++) {
        *command_pointers[i] = 0;
    }

    // SET UP OUTPUT
    pinMode(OUTPIN0, OUTPUT); //designates OUTPIN0 pin to be an output
    pinMode(OUTPIN1, OUTPUT); //designates OUTPIN1 pin to be an input
    pinMode(OUTPIN2, OUTPUT);
    pinMode(OUTPIN3, OUTPUT);
    pinMode(INPIN, INPUT);    //designates INPIN pin to be an input

#ifdef DEBUG
    // REPORT
    Serial.println("botwurst_a ready...");
#endif

}


//////////////////////////////////////
//        WRITE TO PINS             //
//////////////////////////////////////

boolean set_pins() {
    boolean speedValid = 0;
    boolean lengthValid = 0;
    if((wave_speed <= HIGHVOLTAGE) && (wave_speed >= LOWVOLTAGE)){
        speedValid = 1;
    }
    if((wavelength <= HIGHVOLTAGE) && (wavelength >= LOWVOLTAGE)){
        lengthValid = 1;
    }
    if((lengthValid==1) && (speedValid==1)){
        analogWrite(OUTPIN0, wave_speed); //sends "wave_speed" to pin OUTPIN0
        analogWrite(OUTPIN1, wavelength); //sends "wavelength" to pin OUTPIN1
        digitalWrite(OUTPIN2, motor_0);   //sends on or off (0 or 1) to pin OUTPIN2
        digitalWrite(OUTPIN3, motor_1);   //sends on or off (0 or 1) to pin OUTPIN3
        //Serial.print("Reading in voltage: ");
        //Serial.println(digitalRead(INPIN)); //should we ever decide to read in voltages
        return true;
    }
    analogWrite(OUTPIN0, 0); //sends zero voltage, turns off the LED
    analogWrite(OUTPIN1, 0);
    digitalWrite(OUTPIN2, 0);
    digitalWrite(OUTPIN3, 0);
    return false;
}


//////////////////////////////////////
//           MAIN LOOP              //
//////////////////////////////////////

void loop() {
    if (get_motor_command()) {
        //set_pins();
    }
    delay(LOOP_DELAY);
}
