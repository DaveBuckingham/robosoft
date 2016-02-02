//////////////////////////////////////////////////////////////////
//                                                              //
//                       -- BOTWURST C --                       //
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

#define PWM_PIN_0 5
#define PWM_PIN_1 7
#define PWM_PIN_2 9
#define DIRECTION_PIN_0 34
#define DIRECTION_PIN_1 38
#define DIRECTION_PIN_2 42

const byte PWM_PINS[] = {5, 7, 9};
const byte DIRECTION_PINS[] = {34, 38, 42};

#define NUM_SEGMENTS 3
#define NUM_EVENTS (NUM_SEGMENTS * 4)

#define EXPAND 0
#define CONTRACT 1

#define DEFAULT_SPEED 100

char print_buffer[100];



//////////////////////////////////////
//           VARIABLES              //
//////////////////////////////////////

// STORAGE FOR DATA READ FROM SERIAL COM
unsigned char cmd_type;
byte cmd_index;
byte cmd_value;

// MILLISECONDS
unsigned long reference;  // time of start of cycle
unsigned long now;        // time since start of cycle
unsigned long then;       // to check if now has changed
unsigned long pause_start;

byte current_pwms[NUM_SEGMENTS];

byte paused;

byte event_index;

void pause() {
    pause_start = millis();
    analogWrite(PWM_PIN_0, 0);
    analogWrite(PWM_PIN_1, 0);
    analogWrite(PWM_PIN_2, 0);
    paused = 1;
    return;
}

void unpause() {
    reference += (millis() - pause_start);
    //sprintf(print_buffer, "reference: %ul  time: %ul  pause_start: %ul\n", reference, millis(), pause_start);
    //Serial.print(print_buffer);
    analogWrite(PWM_PIN_0, current_pwms[0]);
    analogWrite(PWM_PIN_1, current_pwms[1]);
    analogWrite(PWM_PIN_2, current_pwms[2]);
    paused = 0;
    return;
}

void reset() {
    pause();
    reference = millis();
    then = 0;
    event_index = 0;
}

struct event_s {
    unsigned long time;
    byte motor_index;
    byte direction;
    byte pwm;
    byte skip;
};

struct event_s events[NUM_EVENTS];

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
    pinMode(PWM_PIN_0, OUTPUT);
    pinMode(PWM_PIN_1, OUTPUT);
    pinMode(PWM_PIN_2, OUTPUT);
    pinMode(DIRECTION_PIN_0, OUTPUT);
    pinMode(DIRECTION_PIN_1, OUTPUT);
    pinMode(DIRECTION_PIN_2, OUTPUT);

    for (int i = 0; i < NUM_EVENTS; i++) {
        events[i].time = 99999999999;
        events[i].motor_index = 0;
        events[i].direction = 0;
        events[i].pwm = 0;
        events[i].skip = 0;
    }

    reset();
}


//////////////////////////////////////
//            MAIN LOOP             //
//////////////////////////////////////

void loop() {

    //sprintf(print_buffer, "loop\n");
    //Serial.print(print_buffer);

    //////////////////////////
    //        GAIT          //
    //////////////////////////

    if (!paused) {

        now = millis() - reference;

        if (now > then) {  // its been more than 1 msec
          
            then = now;

            struct event_s *event = &events[event_index];

            if (now >= event->time) {

                sprintf(print_buffer, "index: %d  event_time: %lu  actual_time: %lu  reference: %lu\n", event_index, event->time, now, reference);
                Serial.print(print_buffer);

                if (event->skip) {
                    event->skip = 0;
                }

                else {
                    current_pwms[event->motor_index] = event->pwm;
                    analogWrite(PWM_PINS[event->motor_index], event->pwm);
                    digitalWrite(DIRECTION_PINS[event->motor_index], event->direction);
                }

                event_index++;
                if (event_index == NUM_EVENTS) {
                    event_index = 0;
                    reference = millis();
                    then = 0;
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
        sprintf(print_buffer, "received gait:\n");
        Serial.print(print_buffer);
        for (int i = 0; i < NUM_EVENTS; i++) {
            delay(SERIAL_DELAY);
            read_to_ulong(&events[i].time);
            events[i].motor_index = Serial.read();
            events[i].direction = Serial.read();
            events[i].pwm = Serial.read();
            events[i].skip = Serial.read();
            sprintf(print_buffer, "time: %lu  motor: %d  dir: %d  pwm: %d  skip: %d\n", events[i].time, events[i].motor_index, events[i].direction, events[i].pwm, events[i].skip);
            Serial.print(print_buffer);
        }
        reset();
    }

    //else if (cmd_type == 'r') {
    //    reset();
    //    sprintf(print_buffer, "reset");
    //    Serial.print(print_buffer);
    //}

    //sprintf(print_buffer, "type: %c\n", cmd_type);
    //Serial.print(print_buffer);

}

