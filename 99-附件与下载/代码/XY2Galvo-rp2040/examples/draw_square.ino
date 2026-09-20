/**
 * @file draw_square.ino
 * @author Matthew SYlvester
 * @brief A basic "Hello World" example for the XY2Galvo library.
 * * This sketch initializes the XY2Galvo library and draws a simple
 * square in the center of the projection field. It demonstrates the
 * basic setup and a simple drawing command.
 */

#include <Arduino.h>
#include <XY2Galvo.h>

// Create an instance of the XY2Galvo class
XY2Galvo galvo;

// The library pre-defines some useful laser settings.
// We can access them by declaring them as 'extern'.
// laser_set[0] is for jumping (moving with the laser off).
// laser_set[1] is for drawing fast, straight lines.
// See XY2Galvo.cpp for other predefined settings.
extern LaserSet laser_set[];

void setup() {
  // Start serial communication for debugging if needed
  Serial.begin(115200);
  //add LED indicator
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  // Initialize the PIO state machines and GPIO pins
  galvo.init();
  
  // Start the drawing worker on the second core of the Pico
  galvo.start();
  
  // Wait a moment for everything to settle
  delay(100);

  Serial.println("XY2Galvo library started. Drawing a square.");

  // Define a square to draw. The coordinate system for the scanner
  // ranges from -32767 to +32767 on both axes.
  // Here we define a 20000x20000 unit square centered at (0,0).
  Rect square(10000, -10000, -10000, 10000);

  // Send the command to draw the square to the drawing core.
  // The command is added to a queue and will be processed on core1.
  // We use laser_set[1] for fast, straight lines.
  galvo.drawRect(square, laser_set[1]);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  // The galvo is continuously drawing the geometry sent to it on core1.
  // The main loop on core0 is free to handle other tasks,
  // like checking for user input, updating a display, or sending more
  // drawing commands to the queue.
  
  // For this simple example, we'll just let it run, after pushing onto the queue once
  delay(1000);
}
