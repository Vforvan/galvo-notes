/**
 * @file transformations.ino
 * @author Matthew Sylvester
 * @brief Demonstrates the use of transformations for animation.
 * * This sketch draws a simple square and uses the rotate() and scale()
 * functions inside the main loop to create a continuous spinning
 * and pulsing animation. This shows how to dynamically update the
 * transformation matrix.
 */

#include <Arduino.h>
#include <XY2Galvo.h>
#define GALVO_SPAN  0x10000
// Create an instance of the XY2Galvo class
XY2Galvo galvo;
LaserSet lowspeed = {.speed=50, .pattern=0x3ff, .delay_a=0, .delay_m=0, .delay_e=20};

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  // Initialize and start the galvo worker core
  galvo.init();
  galvo.start();
  delay(100);
  Serial.println("XY2Galvo library started. Transformations demo.");
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  Transformation t{500,500,0,0,0,0};
  galvo.resetTransformation();
  galvo.setTransformation(t);
  galvo.setOffset(-50, 0);
  galvo.printText(Point(0,0), 1, 1, "Hello World!", false, lowspeed, lowspeed);
  digitalWrite(LED_BUILTIN, LOW);
  delay(50);
}
