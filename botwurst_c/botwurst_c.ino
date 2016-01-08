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
#define SERIAL_DELAY 200  // MILLISECONDS
#define BAUD 9600
#define SERIAL_CONFIG SERIAL_8N1

#define PWM_PIN_0 5
#define PWM_PIN_1 7
#define PWM_PIN_2 9
#define DIRECTION_PIN_0 34
#define DIRECTION_PIN_1 38
#define DIRECTION_PIN_2 42

const byte PWM_PINS[] = {5, 7, 9}
const byte DIRECTION_PINS[] = {34, 38, 42}

#define NUM_SEGMENTS 3
#define NUM_EVENTS (NUM_SEGMENTS * 4)

#define EXPAND 0
#define CONTRACT 1

#define DEFAULT_SPEED 100



//////////////////////////////////////
//           VARIABLES              //
//////////////////////////////////////

// STORAGE FOR DATA READ FROM SERIAL COM
char cmd_type;
byte cmd_index;
byte cmd_value;

// MILLISECONDS
unsigned long reference;  // time of start of cycle
unsigned long now;        // time since start of cycle
unsigned long then;       // to check if now has changed

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
    reference += millis() - pause_start;
    analogWrite(PWM_PIN_0, current_pwms[0]);
    analogWrite(PWM_PIN_1, current_pwms[1]);
    analogWrite(PWM_PIN_2, current_pwms[2]);
    paused = 0;
    return;
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
    unsigned long long_number;
};

void read_to_ulong(unsigned long *ulong_pointer) {
    union buffer_u buffer;
    buffer.byte_array[0] = Serial.read();
    buffer.byte_array[1] = Serial.read();
    buffer.byte_array[2] = Serial.read();
    buffer.byte_array[3] = Serial.read();
    *ulong_pointer = buffer.long_number;
    return;
}


//////////////////////////////////////
//           INTIIALIZE             //
//////////////////////////////////////

void setup() {

    pause();
    reference = pause_start;
    event_index = 0;

    // SERIAL COM
    Serial.begin(BAUD, SERIAL_CONFIG);
    
    // GPIO
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
    //        GAIT          //
    //////////////////////////

    if (!paused) {

        now = millis() - reference;

        if (now > then) {  // its been more than 1 msec
          
            then = now;

            struct event_s *event = &events[event_index];

            if (now >= event->time) {

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

    if (cmd_type == 'b') {
        if (cmd_index == 0) {
            analogWrite(PWM_PIN_0, DEFAULT_SPEED);
            digitalWrite(DIRECTION_PIN_0, cmd_value);
        }
        if (cmd_index == 1) {
            analogWrite(PWM_PIN_1, DEFAULT_SPEED);
            digitalWrite(DIRECTION_PIN_1, cmd_value);
        }
        if (cmd_index == 2) {
            analogWrite(PWM_PIN_2, DEFAULT_SPEED);
            digitalWrite(DIRECTION_PIN_2, cmd_value);
        }
        if (cmd_index == 3) {
            if (cmd_value) {
                pause();
            }
            else {
                unpause();
            }
        }
    }

    else if (cmd_type == 't') {
        for (i = 0; i < NUM_EVENTS; i++) {
            read_to_ulong(&events[i].time);
            events[i].motor_index = Serial.read();
            events[i].direction = Serial.read();
            events[i].pwm = Serial.read();
            events[i].skip = Serial.read();
        }
    }

}

