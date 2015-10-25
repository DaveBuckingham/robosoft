#define LOOP_DELAY 100
#define TIMEOUT 1000
#define BAUD 9600

float wave_speed;
float wavelength;
boolean motor_0;
boolean motor_1;

byte read_integer
unsigned long timer;


# LISTEN FOR 10 BYTES
# 8 FOR 2 FLOATS
# 2 FOR 2 INTS
# STORE IN GLOBAL VARIABLES
# RETURN FALSE IF IT TAKES TOO LONG
# OTHERWISE RETURN TRUE
boolean get_motor_command () {
    timer = millis();

    wave_speed = Serial.parseFloat();
    if ((millis - timer) > TIMEOUT) {
        return false;
    }

    wavelength = Serial.parseFloat();
    if ((millis - timer) > TIMEOUT) {
        return false;
    }

    read_integer = Serial.parseInt() ;
    if (((millis - timer) > TIMEOUT) || read_integer == 0) {
        return false
    }
    else {
        motor_0 = read_integer;
    }

    read_integer = Serial.parseInt() ;
    if ((millis - timer) > TIMEOUT) {
        return false;
    }
    else {
        motor_1 = read_integer;
    }
    
    return true;
}


void setup() {
    Serial.begin(BAUD);
    Serial.println("Ready");
}


boolean set_pins() {
    // FOR ALEX
}


void loop() {
    if (get_motor_command) {
        set_pins();
    }
    delay(LOOP_DELAY)
}
