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

// const byte PWM_PINS[] = {5, 7, 9, 11};
// const byte DIRECTION_PINS[] = {32, 34, 36, 38};
const byte PWM_PINS[] = {2, 2, 2, 2};
const byte DIRECTION_PINS[] = {3, 3, 3, 3};

#define NUM_MOTORS 4

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

enum EVENT_TYPE {
    contract,
    contracted,
    expand,
    expanded,
    none
};



struct event_s {
    unsigned long time;
    enum EVENT_TYPE type;
};

struct event_s events[NUM_MOTORS];


int  vars_expanded_delay   [NUM_MOTORS];
int  vars_contract_time    [NUM_MOTORS];
int  vars_contracted_delay [NUM_MOTORS];
int  vars_expand_time      [NUM_MOTORS];
byte vars_contract_speed   [NUM_MOTORS];
byte vars_expand_speed     [NUM_MOTORS];
int  vars_offset           [NUM_MOTORS];



void set_pwm(byte motor, byte speed) {
    current_pwms[motor] = speed;
    analogWrite(PWM_PINS[motor], speed);
}

int read_int() {
    int value = Serial.read();
    value = value << 8;
    return (value | Serial.read());
}

// ONLY CALL AFTER TRANSFER
void reset() {
    for (int motor_i = 0; motor_i < NUM_MOTORS; motor_i++) { 
        events[motor_i].time = millis() + vars_offset[motor_i];
        events[motor_i].type = expanded;
    }
    sprintf(print_buffer, "Reset\n");
    Serial.print(print_buffer);
    pause();
}

void pause() {
    pause_start = millis();

    for (int i = 0; i < NUM_MOTORS; i++) { 
        analogWrite(PWM_PINS[i], 0);
    }

    paused = 1;
    sprintf(print_buffer, "Paused\n");
    Serial.print(print_buffer);
    return;
}

void unpause() {
    int i;
    for (i = 0; i < NUM_MOTORS; i++) {
        events[i].time += (millis() - pause_start);
        analogWrite(PWM_PINS[i], current_pwms[i]);
    }
    paused = 0;
    sprintf(print_buffer, "Unpaused\n");
    Serial.print(print_buffer);
    return;
}



//////////////////////////////////////
//           INTIIALIZE             //
//////////////////////////////////////

void setup() {

    // SERIAL COM
    Serial.begin(BAUD, SERIAL_CONFIG);
    
    for (int motor_i = 0; motor_i < NUM_MOTORS; motor_i++) { 
        // GPIO
        pinMode(PWM_PINS[motor_i], OUTPUT);
        pinMode(DIRECTION_PINS[motor_i], OUTPUT);

        // EVENTS
        for (int event_i = 0; event_i < NUM_MOTORS; event_i++) {
            events[motor_i].time = 0xffffffff;
            events[motor_i].type = none;
        }
    }

    pause();
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


                if (now >= events[motor_i].time) {

                    int error = now - events[motor_i].time;

                    switch (events[motor_i].type) {
                        case contract:
                            sprintf(print_buffer, "Motor %d contract. Error = %d\n", motor_i, error);
                            Serial.print(print_buffer);
                            set_pwm(motor_i, vars_contract_speed[motor_i]);
                            digitalWrite(DIRECTION_PINS[motor_i], CONTRACT);
                            events[motor_i].time = now + vars_contract_time[motor_i];
                            events[motor_i].type = contracted;
                            break;

                        case contracted:
                            sprintf(print_buffer, "Motor %d hold contracted. Error = %d\n", motor_i, error);
                            Serial.print(print_buffer);
                            set_pwm(motor_i, 0);
                            events[motor_i].time = now + vars_contracted_delay[motor_i];
                            events[motor_i].type = expand;
                            break;

                        case expand:
                            sprintf(print_buffer, "Motor %d expand. Error = %d\n", motor_i, error);
                            Serial.print(print_buffer);
                            set_pwm(motor_i, vars_expand_speed[motor_i]);
                            digitalWrite(DIRECTION_PINS[motor_i], EXPAND);
                            events[motor_i].time = now + vars_expand_time[motor_i];
                            events[motor_i].type = expanded;
                            break;

                        case expanded:
                            sprintf(print_buffer, "Motor %d hold expanded. Error = %d\n", motor_i, error);
                            Serial.print(print_buffer);
                            set_pwm(motor_i, 0);
                            events[motor_i].time = now + vars_expanded_delay[motor_i];
                            events[motor_i].type = contract;
                            break;

                        default:
                            sprintf(print_buffer, "Error: unknown event type. Did you transfer a gait?\n");
                            Serial.print(print_buffer);
                            set_pwm(motor_i, 0);
                            break;

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
        if (cmd_index >= 0 && cmd_index < NUM_MOTORS) {
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
        sprintf(print_buffer, "type: %c, index: %d, value: %d\n", cmd_type, cmd_index, cmd_value);
        Serial.print(print_buffer);
    }

    else if (cmd_type == 'p') {
        cmd_value = Serial.read();
        if (cmd_value) {
            unpause();
        }
        else {
            pause();
        }
    }

    else if (cmd_type == 't') {
        sprintf(print_buffer, "received gait:\n");
        Serial.print(print_buffer);

        while (Serial.available() < 12) {
            delay(SERIAL_DELAY);
        }

        for (int motor_i = 0; motor_i < NUM_MOTORS; motor_i++) { 

            vars_expanded_delay[motor_i] = read_int();
            vars_contract_time[motor_i] = read_int();
            vars_contracted_delay[motor_i] = read_int();
            vars_expand_time[motor_i] = read_int();
            vars_contract_speed[motor_i] = Serial.read();
            vars_expand_speed[motor_i] = Serial.read();
            vars_offset[motor_i] = read_int();

            sprintf(print_buffer, "%d %-5d %-5d %-5d %-5d %-3d %-3d %-5d\n",
                                                                            motor_i,
                                                                            vars_expanded_delay[motor_i],
                                                                            vars_contract_time[motor_i],
                                                                            vars_contracted_delay[motor_i],
                                                                            vars_expand_time[motor_i],
                                                                            vars_contract_speed[motor_i],
                                                                            vars_expand_speed[motor_i],
                                                                            vars_offset[motor_i]);
            Serial.print(print_buffer);

        }
        reset();

    }

}

