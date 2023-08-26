// Run "sudo chmod a+rw /dev/ttyACM0" if you get
// the "can't open device: Permission denied error"

#include <Servo.h>
#include <AFMotor.h>
#include <EnableInterrupt.h>
#include "timer.h"
//https://github.com/GreyGnome/EnableInterrupt/wiki/Usage#user-content-disableInterrupt

#define BL_IR A4
#define BR_IR A3

/*
 * Wiring scheme:
 * 
  Y-----                      ----- B
        |--- M1_BL   M4_FL ---|
  w-----                      ----- Y

  Y-----                      ----- B
        |--- M2_BR   M3_FL ---|
  W-----                      ----- Y

*/

AF_DCMotor back_left(1, MOTOR12_2KHZ);     // both are white + yellow
AF_DCMotor back_right(2, MOTOR12_2KHZ);
AF_DCMotor front_right(3, MOTOR34_1KHZ);   // both are blue + yellow
AF_DCMotor front_left(4, MOTOR34_1KHZ);    
Timer timer;
float disk_slots = 20;
float m2_rpm;
int m1_bl, m2_br;
int m1_counter = 0;
int m2_counter = 0;
int counter = 0;


void setup() {
  
//  attachInterrupt(BL_IR, count, RISING);
//  attachPinChangeInterrupt(BR_IR, m2_count, RISING);
  Serial.begin(115200);
//  pinMode(BR_IR, INPUT_PULLUP);
//  enableInterrupt(BR_IR, m2_count, RISING);
//  enableInterrupt(BR_IR, m2_refresh, FALLING);
//  timer.setInterval(1000);
//  timer.setCallback(M2_RPM);
//  timer.start();
}

//TODO: safety controller? It oughta be okay,
//      tutal the point is to detect mirror by itself. 
//      A safety controller during testing to keep 
//      property damage to a minimum should be okay.

void loop() {

  forward();
//  readIRInputData();
//  M2_RPM();
//  Serial.print("M2 counter: ");
//  Serial.println(m2_counter);
//  Serial.print("M2 RPM: ");
//  Serial.println(m2_rpm);
  delay(1000);
  right();
  delay(1000);
  pause();
  delay(1000);
  
}

void m1_count() { m1_counter++; }
void m2_count() { m2_counter++; }
//void m3_count() { m3_counter++; }
//void m4_count() { m4_counter++; }

void m2_refresh() { m2_counter = 0; }

void M2_RPM() {
  m2_rpm = (m2_counter / disk_slots) * 60;
  m2_counter = 0;
}

void readIRInputData() {
//  m1_bl = analogRead(BL_IR);
  m2_br = analogRead(BR_IR);

//  Serial.print(m1_bl);
//  Serial.print(",");
//  Serial.print("M2 analog: ");
//  Serial.println(m2_br);
//  Serial.print("M2_counter: ");
//  Serial.println(m2_counter);
}

// working 10/3
void forward() {

  front_left.setSpeed(100);
  front_right.setSpeed(100);
  back_left.setSpeed(50);
  back_right.setSpeed(50);
  
  front_left.run(FORWARD);
  front_right.run(FORWARD);
  back_left.run(FORWARD);
  back_right.run(FORWARD);

}

// working 10/3
void reverse() {
  
  front_left.setSpeed(50);
  front_right.setSpeed(50);
  back_left.setSpeed(50);
  back_right.setSpeed(50);
  
  front_left.run(BACKWARD);
  front_right.run(BACKWARD);
  back_left.run(BACKWARD);
  back_right.run(BACKWARD);
  
}

// working 10/3, needs some adjustment tho
void left() {
  
  front_left.setSpeed(50);
  front_right.setSpeed(50);
  back_left.setSpeed(70);
  back_right.setSpeed(70);
  
  front_left.run(BACKWARD);
  front_right.run(BACKWARD);
  back_left.run(FORWARD);
  back_right.run(FORWARD);

}

// working 10/3, needs some adjustment
void right() {
  
  front_left.setSpeed(70);
  front_right.setSpeed(90);
  back_left.setSpeed(70);
  back_right.setSpeed(90);
  
  front_left.run(FORWARD);
  front_right.run(FORWARD);
  back_left.run(FORWARD);
  back_right.run(FORWARD);

}
  

void pause() {

//  front_left.setSpeed(0);
//  front_right.setSpeed(0);
//  back_left.setSpeed(0);
//  back_right.setSpeed(0);
  
  front_left.run(RELEASE);
  front_right.run(RELEASE);
  back_left.run(RELEASE);
  back_right.run(RELEASE);

}
