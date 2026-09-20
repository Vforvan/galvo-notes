/**
 * @file drawing_primitives.ino
 * @author Matthew Sylvester
 * @brief Demonstrates various drawing commands in the XY2Galvo library.
 * * This sketch shows how to use different drawing functions like drawLine,
 * drawRect, and drawPolygon to create more complex shapes.
 */

#include <Arduino.h>
#include <XY2Galvo.h>

// Create an instance of the XY2Galvo class
XY2Galvo galvo;

// Access the library's pre-defined laser settings
extern LaserSet laser_set[];

// Define the points for a 5-pointed star shape
const int STAR_POINTS = 10;
Point star[STAR_POINTS] = {
  {0, 20000},
  {4700, 6200},
  {19000, 6200},
  {7600, -2300},
  {11800, -19000},
  {0, -11000},
  {-11800, -19000},
  {-7600, -2300},
  {-19000, 6200},
  {-4700, 6200}
};

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  // Initialize and start the galvo worker core
  galvo.init();
  galvo.start();
  delay(100);

  Serial.println("XY2Galvo library started. Drawing primitives demo.");

  
  // Draw a bounding box for our shapes
  Rect bounds(25000, -25000, -25000, 25000);
  galvo.drawRect(bounds, laser_set[2]); // Use a slower speed for the box

  // Draw two individual lines crossing the box
  galvo.drawLine({-25000, -25000}, {25000, 25000}, laser_set[1]);
  galvo.drawLine({-25000, 25000}, {25000, -25000}, laser_set[1]);
  //draw a circle inscribed within the box
  galvo.drawEllipse(bounds, 0, 100, laser_set[1]);
  // Draw the star shape using the drawPolygon command.
  // drawPolygon is a convenient wrapper around drawPolyLine that
  // automatically closes the shape.
  galvo.drawPolygon(STAR_POINTS, star, laser_set[1]);
  //print some text using vector font
  galvo.printText(Point(0,0),1000, 1000, "TEST", true, laser_set[0], laser_set[1]);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  // All drawing commands have been sent to the queue.
  // The worker on core1 will handle the continuous drawing.
  // The main loop is free.
  delay(1000);
}