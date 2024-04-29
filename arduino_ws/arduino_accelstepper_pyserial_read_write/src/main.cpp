// Receive angle position from laptop as 2 bytes, convert to int, move stepper to that position, and send current motor position to laptop
#include <AccelStepper.h> //include the accelstepper library

// Init constants/variables for serial communication:
// Receive data:
const byte numBytes = 2;
byte received_pkg[numBytes];   // Array to store the received msg
int dataNumber = 0;             // Desired camera position as angle to positive x-axis
bool newData = false;
// Send data:
int pkg_byte_size = 2;
bool send_motor_execution_done_msg = false;

// Define constants for physical setup:
const int steps_per_revolution = 19200; // For NEMA 17 without microstepping
const float gear_ratio = 20.0 / 120.0; // NEMA 17 to rotating plate gear ratio

long total_steps = steps_per_revolution * gear_ratio; // Calculate the total number of steps for a full rotation
const int steps_per_degree = total_steps / 360.0;
long motor_encoder_step_position = 0;

// Init the stepper motor:
#define dirPin 2
#define stepPin 3
#define motorInterfaceType 1

#define MSG_MOTOR_COMMAND_IDX 0
#define MSG_MOTOR_STATUS_REQUESTED_IDX 1

AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

// Setup function: Init serial and set limits for steppermotor:
void setup() {
  Serial.begin(9600);

  stepper.setMaxSpeed(5000);
  stepper.setAcceleration(3000);
}

void read_incoming_pkg() {
  static byte byteIdx = 0;
  byte incoming_byte;

  if (Serial.available() > 0){
    // bool read_pkg_in_progress = true;
    incoming_byte = Serial.read();
    received_pkg[byteIdx] = incoming_byte;
    byteIdx++;

    if (byteIdx >= numBytes)
    {
      byteIdx = 0;
      newData = true;
    }
  }
}

void set_motor_target_pos() {
  if (newData == true) {
    dataNumber = 0;
    // dataNumber = atoi(receivedChars);   // convert received msg (desired camera angle postion) to int
    dataNumber = int((received_pkg[0] << 8) | received_pkg[1] );  // convert received msg (desired camera angle postion) to int

    // Convert desired camera position to motor position (encoder position in steps):
    motor_encoder_step_position = steps_per_degree * dataNumber;

    // Update flags:
    newData = false;
    send_motor_execution_done_msg = true;
  }
}

void run_stepper() {
  // run stepper motor to desired camera position (blocking call):
  stepper.runToNewPosition(motor_encoder_step_position);
}

void send_motor_pos_to_pc(){
  if (send_motor_execution_done_msg == true){
    // Send msg to pc with currrent angle position of the stepper motor to confirm motor has moved to the correct position.
    int reached_camera_position = stepper.currentPosition() / steps_per_degree;

    if (Serial.availableForWrite() > pkg_byte_size - 1){
      byte out_buff[pkg_byte_size] = {lowByte(reached_camera_position), highByte(reached_camera_position)};
      Serial.write(out_buff, pkg_byte_size);
      Serial.flush();
      send_motor_execution_done_msg = false;
    }
  }
}

void loop() {
  read_incoming_pkg();
  set_motor_target_pos();
  run_stepper();
  send_motor_pos_to_pc();
}