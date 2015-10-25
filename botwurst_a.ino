#define LOOP_DELAY 100
#define TIMEOUT 1000
#define BAUD 9600
#define SERIAL_CONFIG SERIAL_8N1

float wave_speed;
float wavelength;
boolean motor_0;
boolean motor_1;

byte read_integer
unsigned long timer;
char read_char


# LISTEN FOR 10 BYTES
# 8 FOR 2 FLOATS
# 2 FOR 2 INTS
# STORE IN GLOBAL VARIABLES
# RETURN FALSE IF IT TAKES TOO LONG
# OTHERWISE RETURN TRUE
boolean get_motor_command () {
    timer = millis();

    # IF THERE ARE INCOMMING BYTES
    # WAIT SO ALL THE DATA CAN ARRIVE
    # READ UNTIL START BYTE IE ':'
    if (Serial.available()){
        read_char = Serial.read();
        delay(100); // Wait for all data.
        while (read_char != ':') {
            if (! Serial.available()) {
                return false;
            }
            read_char = Serial.read();
        }
    }
    else {
        return false;
    }

    if ((millis() - timer) > TIMEOUT) {
        return false;
    }

    wave_speed = Serial.parseFloat();
    if ((millis() - timer) > TIMEOUT) {
        return false;
    }

    wavelength = Serial.parseFloat();
    if ((millis() - timer) > TIMEOUT) {
        return false;
    }

    read_integer = Serial.parseInt() ;
    if (((millis() - timer) > TIMEOUT) || read_integer == 0) {
        return false
    }
    else {
        motor_0 = read_integer;
    }

    read_integer = Serial.parseInt() ;
    if (((millis() - timer) > TIMEOUT) || read_integer == 0) {
        return false;
    }
    else {
        motor_1 = read_integer;
    }
    
    return true;

# WILL I HAVE TO DO SOMETHING LIKE THIS?
# https://gist.github.com/toddstavish/534615
#unsigned long readULongFromBytes() {
#  union u_tag {
#    byte b[4];
#    unsigned long ulval;
#  } u;
#  u.b[0] = Serial.read();
#  u.b[1] = Serial.read();
#  u.b[2] = Serial.read();
#  u.b[3] = Serial.read();
#  return u.ulval;
#}
#unsigned long val = readULongFromBytes();
#Serial.print(val, DEC); // send to python to checkj


}


void setup() {
    Serial.begin(BAUD);
    Serial.println("Ready");  // we might want to read this
}


boolean set_pins() {
    // FOR ALEX
}


void loop() {
    if (get_motor_command) {
        // set_pins();
        
        // FOR TESTING
        delay(100);
        Serial.print(wave_speed);
        Serial.print("\t");
        Serial.print(wavelength);
        Serial.print("\t");
        Serial.print(motor_0);
        Serial.print("\t");
        Serial.print(motor_1);
        Serial.println("\t");

    }
    delay(LOOP_DELAY)
}
