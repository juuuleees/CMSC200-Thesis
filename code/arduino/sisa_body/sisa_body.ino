// Run "sudo chmod a+rw /dev/ttyACM0" if you get
// the "can't open device: Permission denied error"

#include <Servo.h>
#include <AFMotor.h>

AF_DCMotor front_left(1, MOTOR12_1KHZ);    // red+orange
AF_DCMotor front_right(2, MOTOR12_1KHZ);   // blue+green
AF_DCMotor back_right(3, MOTOR12_1KHZ);
AF_DCMotor back_left(4, MOTOR12_1KHZ);     // both are blue+orange

void setup() {

}

void loop() {

  pause();
  delay(1000);
//  forward();
//  delay(1000);
//  reverse();
//  delay(1000);
//  left();
//  delay(1000);
  right();
  delay(1000);

}

// working 10/3
void forward() {

  front_left.setSpeed(100);
  front_right.setSpeed(100);
  back_left.setSpeed(100);
  back_right.setSpeed(100);
  
  front_left.run(FORWARD);
  front_right.run(FORWARD);
  back_left.run(FORWARD);
  back_right.run(FORWARD);

}

// working 10/3
void reverse() {
  
  front_left.setSpeed(100);
  front_right.setSpeed(100);
  back_left.setSpeed(100);
  back_right.setSpeed(100);
  
  front_left.run(BACKWARD);
  front_right.run(BACKWARD);
  back_left.run(BACKWARD);
  back_right.run(BACKWARD);
  
}

// working 10/3, needs some adjustment tho
void left() {
  
  front_left.setSpeed(100);
  front_right.setSpeed(100);
  back_left.setSpeed(200);
  back_right.setSpeed(200);
  
  front_left.run(BACKWARD);
  front_right.run(BACKWARD);
  back_left.run(FORWARD);
  back_right.run(FORWARD);

}

// working 10/3, needs some adjustment
void right() {
  
  front_left.setSpeed(100);
  front_right.setSpeed(0);
  back_left.setSpeed(100);
  back_right.setSpeed(100);
  
  front_left.run(FORWARD);
  front_right.run(FORWARD);
  back_left.run(FORWARD);
  back_right.run(FORWARD);

}
  

void pause() {

  front_left.setSpeed(0);
  front_right.setSpeed(0);
  back_left.setSpeed(0);
  back_right.setSpeed(0);
  
  front_left.run(RELEASE);
  front_right.run(RELEASE);
  back_left.run(RELEASE);
  back_right.run(RELEASE);

}
