//////////////////////////////////////////////////////////////////
//                                                              //
//                       -- BOTWURST D --                       //
//                                                              //
//                       DAVE BUCKINGHAM                        //
//                                                              //
//////////////////////////////////////////////////////////////////


//////////////////////////////////////
//            CONSTANTS             //
//////////////////////////////////////

// SERIAL COM
#define SERIAL_DELAY 100  // MILLISECONDS
#define BAUD 9600
#define SERIAL_CONFIG SERIAL_8N1

const byte PWM_PINS[] = {5, 7, 9, 11};
const byte DIRECTION_PINS[] = {32, 34, 36, 38};

#define NUM_MOTORS 4
#define EVENTS_PER_MOTOR 4

#define EXPAND 0
#define CONTRACT 1

#define DEFAULT_SPEED 100

char print_buffer[300];



//////////////////////////////////////
//           VARIABLES              //
//////////////////////////////////////

// STORAGE FOR DATA READ FROM SERIAL COM
unsigned char cmd_type;
byte cmd_index;
byte cmd_value;

// MILLISECONDS
unsigned long reference[NUM_MOTORS];  // time of start of cycle
unsigned long now;        // time since start of cycle
unsigned long then;       // to check if now has changed
unsigned long pause_start;

byte current_pwms[NUM_MOTORS];

byte paused;


struct event_s {
    unsigned long time;
    byte direction;
    byte pwm;
};



struct event_s events[NUM_MOTORS][EVENTS_PER_MOTOR];
byte event_index[NUM_MOTORS];

void pause() {
    pause_start = millis();

    for (int i = 0; i < NUM_MOTORS; i++) { 
        analogWrite(PWM_PINS[i], 0);
    }


    paused = 1;
    return;
}

void unpause() {
    int i;
    for (i = 0; i < NUM_MOTORS; i++) {
        reference[i] += (millis() - pause_start);
        analogWrite(PWM_PINS[i], current_pwms[i]);
    }
    paused = 0;
    return;
}

void reset() {
    for (int i = 0; i < NUM_MOTORS; i++) {
        reference[i] = millis();
        event_index[i] = 0;
    }
    then = 0;
    // if pause isn't last, possible off by one
    // error leading to large (now - reference)
    // at start of gait? maybe?
    pause();
}



union buffer_u {
    byte byte_array[4];
    unsigned long value;
};

void read_to_ulong(unsigned long *ulong_pointer) {
    union buffer_u buffer;
    buffer.byte_array[3] = Serial.read();
    buffer.byte_array[2] = Serial.read();
    buffer.byte_array[1] = Serial.read();
    buffer.byte_array[0] = Serial.read();
    *ulong_pointer = buffer.value;
    return;
}


//////////////////////////////////////
//           INTIIALIZE             //
//////////////////////////////////////

void setup() {

    // SERIAL COM
    Serial.begin(BAUD, SERIAL_CONFIG);
    
    // GPIO
    for (int motor_i = 0; motor_i < NUM_MOTORS; motor_i++) { 
        pinMode(PWM_PINS[motor_i], OUTPUT);
        pinMode(DIRECTION_PINS[motor_i], OUTPUT);

        for (int event_i = 0; event_i < EVENTS_PER_MOTOR; event_i++) {
            events[motor_i][event_i].time = 99999999999;
            events[motor_i][event_i].direction = 0;
            events[motor_i][event_i].pwm = 0;
        }
    }

    reset();
}


//////////////////////////////////////
//            MAIN LOOP             //
//////////////////////////////////////

void loop() {


    //////////////////////////
    //        GAIT          //
    //////////////////////////

    if (!paused) {

        now = millis();


        if (now > then) {  // its been more than 1 msec
          
            then = now;


            for (int motor_i = 0; motor_i < NUM_MOTORS; motor_i++) {

                struct event_s *event = &events[motor_i][event_index[motor_i]];



                if (now - reference[motor_i] >= event->time) {

                    int error = now - reference[motor_i] - event->time;
                    sprintf(print_buffer, "motor: %d   event: %d   time: %d   error: %d\n",
                                                                                            motor_i,
                                                                                            event_index[motor_i],
                                                                                            event->time,
                                                                                            error);
                    Serial.print(print_buffer);
                    current_pwms[motor_i] = event->pwm;
                    analogWrite(PWM_PINS[motor_i], event->pwm);
                    digitalWrite(DIRECTION_PINS[motor_i], event->direction);

                    event_index[motor_i]++;
                    if (event_index[motor_i] == EVENTS_PER_MOTOR) {
                        event_index[motor_i] = 0;
                        reference[motor_i] = millis();
                    }
                }
            }
        }
    }


    //////////////////////////
    // RECEIVE TRANSMISSION //
    //////////////////////////

    // READ TYPE
    if (! Serial.available()) {
        return;
    }
    cmd_type = Serial.read();
    delay(SERIAL_DELAY);


    if (cmd_type == 'a') {
        cmd_index = Serial.read();
        if (cmd_index >= 0 && cmd_index < 3) {
	    cmd_value = Serial.read();
            if (cmd_value == 0) {
                analogWrite(PWM_PINS[cmd_index], 0);
            }
            else if (cmd_value == 1) {
                analogWrite(PWM_PINS[cmd_index], DEFAULT_SPEED);
                digitalWrite(DIRECTION_PINS[cmd_index], CONTRACT);
            }
            else if (cmd_value == 2) {
                analogWrite(PWM_PINS[cmd_index], DEFAULT_SPEED);
                digitalWrite(DIRECTION_PINS[cmd_index], EXPAND);
            }
        }
        if (cmd_index == 3) {
	    cmd_value = Serial.read();
            if (cmd_value) {
                unpause();
            }
            else {
                pause();
            }
        }
        sprintf(print_buffer, "type: %c, index: %d, value: %d\n", cmd_type, cmd_index, cmd_value);
        Serial.print(print_buffer);
    }

    else if (cmd_type == 't') {
        reset();  // zeros all event_index[]
        sprintf(print_buffer, "received gait:\n");
        Serial.print(print_buffer);

        int num_events = EVENTS_PER_MOTOR * NUM_MOTORS;
        while (num_events--) {
            delay(SERIAL_DELAY);
            int motor_i = Serial.read();
            if (motor_i >= NUM_MOTORS) {
                sprintf(print_buffer, "motor index exceeds num motors: %d\n", motor_i);
                Serial.print(print_buffer);
                motor_i = 0;
            }

            unsigned long time;
            read_to_ulong(&time);
            int direction = Serial.read();
            int pwm = Serial.read();
            sprintf(print_buffer, "time: %lu  motor: %d  dir: %d  pwm: %d\n", time, motor_i, direction, pwm);
            Serial.print(print_buffer);

            events[motor_i][event_index[motor_i]].time = time;
            events[motor_i][event_index[motor_i]].direction = direction;
            events[motor_i][event_index[motor_i]].pwm = pwm;
            event_index[motor_i]++;


        }

        for (int i = 0; i < NUM_MOTORS; i++) {
            event_index[i] = 0;
        }

    }

    //else if (cmd_type == 'r') {
    //    reset();
    //    sprintf(print_buffer, "reset");
    //    Serial.print(print_buffer);
    //}

    //sprintf(print_buffer, "type: %c\n", cmd_type);
    //Serial.print(print_buffer);

}

