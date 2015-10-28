#define LOOP_DELAY 100
#define TIMEOUT 1000
#define BAUD 9600
#define SERIAL_CONFIG SERIAL_8N1
#define LOWVOLTAGE 0   //the low boundary for output voltage
#define HIGHVOLTAGE 255 //the high boundary for output voltage

//In general, designated output pins send voltage out from the arduino to connected devices
//For testing, pin 13 has an LED that will turn on with a certain voltage sent out
//The analog pins on the Mega are A0-A5
#define OUTPIN A0
//In general, if we ever want to read voltages in from the arduino to get feedback from
//the robot, it can be done using the input pins
#define INPIN 12

# IN FACT THESE ARE EACH 8 BITS
byte wave_speed;
byte wavelength;
boolean motor_0;
boolean motor_1;

byte read_integer
unsigned long timer;
char read_char


# LISTEN FOR 4 BYTES
# STORE IN GLOBAL VARIABLES
# RETURN FALSE IF IT TAKES TOO LONG
# OTHERWISE RETURN TRUE
boolean get_motor_command () {
    timer = millis();

    # IF THERE ARE INCOMMING BYTES
    # WAIT SO ALL THE DATA CAN ARRIVE
    # CHECK FOR START FLAG ':'
    if (! Serial.available()) {
        return false;
    }
    read_char = Serial.read();
    delay(100);  // Wait for all data
    while (read_char != ':' && Serial.available()) {
        read_char = Serial.read();
    }
    if (read_char != ':') {
        return false;
    }


    if ((millis() - timer) > TIMEOUT) { return false; }

    wave_speed = Serial.parseInt();
    if ((millis() - timer) > TIMEOUT) { return false; }

    wavelength = Serial.parseInt();
    if ((millis() - timer) > TIMEOUT) { return false; }

    motor_0 = Serial.parseInt();
    if ((millis() - timer) > TIMEOUT) { return false; }

    motor_1 = Serial.parseInt();
    if ((millis() - timer) > TIMEOUT) { return false; }

    return true;
}


void setup() {
    Serial.begin(BAUD);
    Serial.println("Ready");  // we might want to read this
    pinMode(OUTPIN, OUTPUT);  //designates OUTPIN pin to be an output
    pinMode(INPIN, INPUT);    //designates INPIN pin to be an input
}


boolean set_pins() {
    float voltage = wave_speed*wavelength;
    if((voltage <= HIGHVOLTAGE) && (voltage >= LOWVOLTAGE)){
        digitalWrite(OUTPIN, voltage); //sends "voltage" to pin OUTPIN, which turns LED on
        //Serial.print("Reading in voltage: ");
        //Serial.println(digitalRead(INPIN)); //should we ever decide to read in voltages
        return true;
    }
    digitalWrite(OUTPIN, 0); //sends zero voltage, turns off the LED
    return false;
}


void loop() {
    if (get_motor_command) {
        set_pins();
        
        // FOR TESTING
        //delay(LOOP_DELAY);
        //Serial.print(wave_speed);
        //Serial.print("\t");
        //Serial.print(wavelength);
        //Serial.print("\t");
        //Serial.print(motor_0);
        //Serial.print("\t");
        //Serial.print(motor_1);
        //Serial.println("\t");

    }
    delay(LOOP_DELAY)
}
