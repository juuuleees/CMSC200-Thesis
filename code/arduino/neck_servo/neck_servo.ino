#include <Servo.h>

Servo neck;
const int RIGHT_SPD = 80;
const int LEFT_SPD = 120;
const int STOPPED = 90;
int pos = 0;
int milliseconds = 5;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  neck.attach(10);
}

void loop() {
// 0 in one direction, 180 in the other direction
// 90 to stop
// delay for continous servers is how long it'll run

  neck.write(RIGHT_SPD);
  delay(1000);
  neck.write(STOPPED);
  delay(1000);
  neck.write(LEFT_SPD);
  delay(1000);

//  I'm annoyed at what a boba shit implementation this coulda been
}
