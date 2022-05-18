//input example: (motornumber),(numberofsteps)/n

#include <stdio.h>
#include <string.h>
#include <Arduino.h>
#include <AFMotor.h>

const int stepsPerRevolution = 10;

AF_Stepper motor1(stepsPerRevolution, 1);
AF_Stepper motor2(stepsPerRevolution, 2);

char str2[10]; //space allocated to str2: 20
char *str[2]; // space allocated to str: 2
char *data = NULL; //initiate char data variable

void setup() {
  Serial.begin(9600);
  motor1.setSpeed(600); // 30rpm
  motor2.setSpeed(600);
  //Serial.println("ready");
}

void loop() {
  if (Serial.available() > 0) { //if input from rpi, do
    String str1 = Serial.readStringUntil("/n"); //readStringUntil to ensure readstring cuts off after 2 numbers
    str1.toCharArray(str2, 20); // convert from string to char array
    byte index = 0;
    data = strtok(str2, ","); // seperate input by commas
    while (data != NULL) { // break down char string into array of char numbers
      str[index] = data;
      index++;
      data = strtok(NULL, ",");
    }
    int s = atoi(str[0]); // convert char to int, will not work for numbers with more than 9 digits
    int y = atoi(str[1]);
    if (s == 1) {
      motor1.step(y, FORWARD, SINGLE);
    }
    if (s == 2) {
      motor2.step(y, FORWARD, SINGLE);  
    } 
    if (s == 3) {
      motor1.step(y, FORWARD, SINGLE);
    }
    if (s == 4) {
      motor2.step(y, FORWARD, SINGLE);  
    }
    Serial.println("complete");
  }
}
